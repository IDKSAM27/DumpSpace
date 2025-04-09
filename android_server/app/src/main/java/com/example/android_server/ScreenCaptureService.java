package com.example.android_server;

import android.app.Activity;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.graphics.PixelFormat;
import android.hardware.display.DisplayManager;
import android.hardware.display.VirtualDisplay;
import android.media.Image;
import android.media.ImageReader;
import android.media.projection.MediaProjection;
import android.media.projection.MediaProjectionManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Surface;
import android.view.WindowManager;
import android.graphics.Bitmap;

import java.io.ByteArrayOutputStream;
import java.nio.ByteBuffer;
import java.util.Timer;
import java.util.TimerTask;

public class ScreenCaptureService extends Service {
    private static final String TAG = "AndroidServer";

    private MediaProjection mediaProjection;
    private ImageReader imageReader;
    private VirtualDisplay virtualDisplay;
    private ScreenStreamingServer streamingServer;
    private Timer heartbeatTimer;
    private ScreenEncoder screenEncoder;


    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        Log.d(TAG, "ScreenCaptureService: onStartCommand called");

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            NotificationChannel channel = new NotificationChannel(
                    "screen_capture",
                    "Screen Capture",
                    NotificationManager.IMPORTANCE_LOW
            );
            NotificationManager manager = getSystemService(NotificationManager.class);
            manager.createNotificationChannel(channel);

            Notification notification = new Notification.Builder(this, "screen_capture")
                    .setContentTitle("Screen Capture Running")
                    .setContentText("Your screen is being shared")
                    .setSmallIcon(R.drawable.ic_launcher_foreground)
                    .build();

            startForeground(1, notification, ServiceInfo.FOREGROUND_SERVICE_TYPE_MEDIA_PROJECTION);
        } else {
            startForeground(1, new Notification());
        }

        int resultCode = intent.getIntExtra("resultCode", Activity.RESULT_CANCELED);
        Intent data = intent.getParcelableExtra("data");

        if (resultCode == Activity.RESULT_OK && data != null) {
            Log.d(TAG, "ScreenCaptureService: Starting MediaProjection");

            MediaProjectionManager projectionManager =
                    (MediaProjectionManager) getSystemService(MEDIA_PROJECTION_SERVICE);
            mediaProjection = projectionManager.getMediaProjection(resultCode, data);

            // ✅ Start the encoder
            screenEncoder = new ScreenEncoder();
            screenEncoder.startEncoding();

            // ✅ Create virtual display with encoder's input surface
            DisplayMetrics metrics = new DisplayMetrics();
            WindowManager wm = (WindowManager) getSystemService(WINDOW_SERVICE);
            wm.getDefaultDisplay().getRealMetrics(metrics);

            Surface inputSurface = screenEncoder.getInputSurface();
            mediaProjection.createVirtualDisplay(
                    "ScreenCapture",
                    metrics.widthPixels,
                    metrics.heightPixels,
                    metrics.densityDpi,
                    DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
                    inputSurface,
                    null,
                    null
            );

            // ✅ Start the streaming server
            streamingServer = new ScreenStreamingServer();
            streamingServer.startServer();

            // ✅ Start a thread to read encoded H.264 frames and send
            new Thread(() -> {
                while (true) {
                    if (screenEncoder != null) {
                        for (byte[] frame : screenEncoder.getEncodedFrames()) {
                            streamingServer.sendFrame(frame);
                        }
                    }
                }
            }).start();
        } else {
            Log.e(TAG, "ScreenCaptureService: Missing permission data!");
            stopSelf();
        }

        // ✅ Optional heartbeat
        startHeartbeat();

        return START_NOT_STICKY;
    }


    private void startScreenCapture() {
        Log.d(TAG, "ScreenCaptureService: Setting up screen capture");

        DisplayMetrics metrics = new DisplayMetrics();
        WindowManager windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
        windowManager.getDefaultDisplay().getMetrics(metrics);

        int width = metrics.widthPixels;
        int height = metrics.heightPixels;
        int density = metrics.densityDpi;

        imageReader = ImageReader.newInstance(width, height, PixelFormat.RGBA_8888, 2);
        Surface surface = imageReader.getSurface();

        virtualDisplay = mediaProjection.createVirtualDisplay(
                "ScreenCapture",
                width, height, density,
                DisplayManager.VIRTUAL_DISPLAY_FLAG_AUTO_MIRROR,
                surface, null, null
        );

        imageReader.setOnImageAvailableListener(reader -> {
            Image image = reader.acquireLatestImage();
            if (image != null) {
                sendFrame(image);
                image.close();
            }
        }, null);

        Log.d(TAG, "ScreenCaptureService: Virtual display and image reader started");

        // Start the streaming server
        streamingServer = new ScreenStreamingServer();
        streamingServer.startServer();

        Log.d(TAG, "ScreenCaptureService: Streaming server started");
    }

    private void sendFrame(Image image) {
        try {
            Image.Plane[] planes = image.getPlanes();
            ByteBuffer buffer = planes[0].getBuffer();
            int width = image.getWidth();
            int height = image.getHeight();

            Bitmap bitmap = Bitmap.createBitmap(width, height, Bitmap.Config.ARGB_8888);
            bitmap.copyPixelsFromBuffer(buffer);

            ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
            bitmap.compress(Bitmap.CompressFormat.JPEG, 50, outputStream);
            byte[] jpegData = outputStream.toByteArray();

            if (streamingServer != null) {
                streamingServer.sendFrame(jpegData);
            }
        } catch (Exception e) {
            Log.e(TAG, "ScreenCaptureService: Error in sendFrame: " + e.getMessage());
        }
    }

    private void startHeartbeat() {
        heartbeatTimer = new Timer();
        heartbeatTimer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {
                Log.d(TAG, "ScreenCaptureService: Heartbeat - service running");
            }
        }, 0, 5000); // every 5 seconds
    }

    @Override
    public void onDestroy() {
        Log.d(TAG, "ScreenCaptureService: onDestroy called");
        super.onDestroy();

        if (mediaProjection != null) {
            mediaProjection.stop();
            mediaProjection = null;
        }

        if (virtualDisplay != null) {
            virtualDisplay.release();
            virtualDisplay = null;
        }

        if (streamingServer != null) {
            streamingServer.stopServer();
            streamingServer = null;
        }

        if (heartbeatTimer != null) {
            heartbeatTimer.cancel();
        }

        Log.d(TAG, "ScreenCaptureService: Cleaned up everything");
    }
}
