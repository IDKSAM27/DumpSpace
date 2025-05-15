package com.example.android_server;

import android.util.Log;

import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class ScreenStreamingServer {
    private static final String TAG = "ScreenStreamingServer";
    private static final int PORT = 8080;

    private ServerSocket serverSocket;
    private Socket clientSocket;
    private OutputStream outputStream;
    private volatile boolean isRunning = false;

    public void startServer() {
        new Thread(() -> {
            try {
                serverSocket = new ServerSocket(PORT);
                isRunning = true;
                Log.d(TAG, "Server started on port " + PORT + ", waiting for connection...");

                clientSocket = serverSocket.accept();
                Log.d(TAG, "Client connected from " + clientSocket.getInetAddress());

                outputStream = clientSocket.getOutputStream();

            } catch (Exception e) {
                Log.e(TAG, "Error starting server: " + e.getMessage(), e);
                isRunning = false;
            }
        }).start();
    }

    public void sendFrame(byte[] data) {
        try {
            if (outputStream != null && isRunning) {
                outputStream.write(data);
                outputStream.flush();
                Log.d(TAG, "Sent frame of size: " + data.length);
            } else {
                Log.d(TAG, "OutputStream is null or server not running");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error sending frame: " + e.getMessage(), e);
            isRunning = false;
        }
    }

    public void stopServer() {
        try {
            isRunning = false;
            if (outputStream != null) outputStream.close();
            if (clientSocket != null) clientSocket.close();
            if (serverSocket != null) serverSocket.close();
            Log.d(TAG, "Server stopped");
        } catch (Exception e) {
            Log.e(TAG, "Error stopping server: " + e.getMessage(), e);
        }
    }
}
