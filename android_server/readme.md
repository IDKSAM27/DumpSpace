# android_server

**`android_server`** is an Android application that captures the device's screen in real-time, encodes it using H.264, and streams the video to a connected client over a local socket. It leverages Android’s `MediaProjection` API for screen capture and `MediaCodec` for hardware-accelerated encoding.

## Features

-  Real-time screen capture using `MediaProjection`
-  Hardware-accelerated H.264 encoding with `MediaCodec`
-  Local socket-based video streaming server (`ServerSocket`)
-  Background foreground service support for Android 10+
-  Modular architecture with clear separation of concerns

---

##  Getting Started

### Prerequisites

- Android Studio installed
- Android device or emulator with **API 21 (Lollipop)** or higher
- Permission to capture screen (granted at runtime)

### Building the App

1. Clone this repository:

    ```bash
    git clone https://github.com/yourusername/android_server.git
    cd android_server
    ```

2. Open the project in Android Studio.

3. Build and run on a physical Android device.

---

##  How It Works

1. **MainActivity** requests screen capture permissions via `MediaProjectionManager`.
2. Upon approval, it starts the **ScreenCaptureService** as a foreground service.
3. **ScreenCaptureService**:
   - Sets up `MediaProjection` and a virtual display.
   - Passes the display output to a `MediaCodec` encoder via `Surface`.
   - Streams H.264-encoded frames to a connected client via `ServerSocket`.

---

##  Key Classes & Responsibilities

| Class | Description |
|-------|-------------|
| `MainActivity` | Requests MediaProjection permissions and starts the capture service |
| `ScreenCaptureService` | Sets up the media projection and streaming server, manages lifecycle |
| `ScreenEncoder` | Configures and runs the H.264 encoder using `MediaCodec` |
| `ScreenStreamingServer` | Runs a TCP server that sends encoded frames to the connected client |

---

##  Streaming Details

- Server listens on `port 8080`.
- First client that connects receives a continuous stream of encoded H.264 frames.
- Client must handle decoding of raw H.264 frames.

>  No framing or protocol like RTSP/HTTP is used — this is a raw TCP stream.

---

##  Known Limitations

- Only one client can be connected at a time.
- No reconnection or frame metadata (e.g. SPS/PPS headers) handling.
- Network interface binding is not customizable.
- No UI – it's permission-driven and auto-starts.

---

##  Testing

You can test this project by (making changes):
- Connecting a custom H.264-compatible client (e.g. FFmpeg, GStreamer, or VLC with a proper wrapper).
- Writing a desktop application that connects to `PORT 8080` and decodes H.264 streams.

---

##  Permissions

- `MEDIA_PROJECTION`: Requested at runtime
- `FOREGROUND_SERVICE`: For persistent background execution
- No other dangerous permissions required

---

##  License

[MIT License](https://github.com/IDKSAM27/DumpSpace/tree/main/android_server/LICENSE) – feel free to use and modify this project.

---

##  Acknowledgments

- Android `MediaProjection` & `MediaCodec` APIs
- Java Sockets for lightweight network transport
- Inspiration from lightweight screen streaming use cases (scrcpy)

---

##  Contact

For questions, issues, or suggestions, feel free to open an issue or contact [me](mailto:sampreetpatil@proton.me).
