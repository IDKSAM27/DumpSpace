package com.example.android_server;

import android.media.MediaCodec;
import android.media.MediaCodecInfo;
import android.media.MediaFormat;
import android.util.Log;
import android.view.Surface;

import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;

public class ScreenEncoder {
    private static final String TAG = "ScreenEncoder";
    private static final String MIME_TYPE = "video/avc"; // H.264
    private static final int WIDTH = 1280;
    private static final int HEIGHT = 720;
    private static final int FRAME_RATE = 30;
    private static final int BIT_RATE = 5_000_000;
    private static final int I_FRAME_INTERVAL = 2;

    private MediaCodec mediaCodec;
    private Surface inputSurface;

    public ScreenEncoder() {
        try {
            MediaFormat format = MediaFormat.createVideoFormat(MIME_TYPE, WIDTH, HEIGHT);
            format.setInteger(MediaFormat.KEY_COLOR_FORMAT, MediaCodecInfo.CodecCapabilities.COLOR_FormatSurface);
            format.setInteger(MediaFormat.KEY_BIT_RATE, BIT_RATE);
            format.setInteger(MediaFormat.KEY_FRAME_RATE, FRAME_RATE);
            format.setInteger(MediaFormat.KEY_I_FRAME_INTERVAL, I_FRAME_INTERVAL);

            mediaCodec = MediaCodec.createEncoderByType(MIME_TYPE);
            mediaCodec.configure(format, null, null, MediaCodec.CONFIGURE_FLAG_ENCODE);
            inputSurface = mediaCodec.createInputSurface(); // <-- this is what you'll use with VirtualDisplay
        } catch (IOException e) {
            Log.e(TAG, "Failed to initialize MediaCodec", e);
        }
    }

    public Surface getInputSurface() {
        return inputSurface;
    }

    public void startEncoding() {
        if (mediaCodec != null) {
            mediaCodec.start();
        }
    }

    public List<byte[]> getEncodedFrames() {
        List<byte[]> encodedFrames = new ArrayList<>();
        MediaCodec.BufferInfo bufferInfo = new MediaCodec.BufferInfo();

        int outputIndex;
        while ((outputIndex = mediaCodec.dequeueOutputBuffer(bufferInfo, 0)) >= 0) {
            ByteBuffer outputBuffer = mediaCodec.getOutputBuffer(outputIndex);
            if (outputBuffer != null && bufferInfo.size > 0) {
                byte[] data = new byte[bufferInfo.size];
                outputBuffer.get(data);
                encodedFrames.add(data);
            }
            mediaCodec.releaseOutputBuffer(outputIndex, false);
        }

        return encodedFrames;
    }

    public void stopEncoding() {
        if (mediaCodec != null) {
            mediaCodec.stop();
            mediaCodec.release();
        }
    }
}
