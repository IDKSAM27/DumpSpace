package com.example.android_server;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.media.projection.MediaProjectionManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private static final int REQUEST_CODE = 1000;
    private static final String TAG = "AndroidServer";

    @RequiresApi(api = Build.VERSION_CODES.LOLLIPOP)
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        Log.d(TAG, "MainActivity: onCreate called");

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            Log.d(TAG, "MainActivity: Requesting MediaProjection permission...");
            MediaProjectionManager mProjectionManager =
                    (MediaProjectionManager) getSystemService(Context.MEDIA_PROJECTION_SERVICE);

            Intent captureIntent = mProjectionManager.createScreenCaptureIntent();
            startActivityForResult(captureIntent, REQUEST_CODE);
        } else {
            Log.e(TAG, "MainActivity: Android version not supported");
            Toast.makeText(this, "Your Android version is not supported", Toast.LENGTH_SHORT).show();
            finish();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == REQUEST_CODE) {
            if (resultCode == Activity.RESULT_OK && data != null) {
                Log.d(TAG, "MainActivity: MediaProjection permission granted");

                Intent serviceIntent = new Intent(this, ScreenCaptureService.class);
                serviceIntent.putExtra("resultCode", resultCode);
                serviceIntent.putExtra("data", data);

                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    Log.d(TAG, "MainActivity: Starting ScreenCaptureService (foreground)");
                    startForegroundService(serviceIntent);
                } else {
                    Log.d(TAG, "MainActivity: Starting ScreenCaptureService (background)");
                    startService(serviceIntent);
                }

                finish();
            } else {
                Log.e(TAG, "MainActivity: MediaProjection permission denied");
                Toast.makeText(this, "Screen capture permission denied", Toast.LENGTH_SHORT).show();
                finish();
            }
        }
    }
}
