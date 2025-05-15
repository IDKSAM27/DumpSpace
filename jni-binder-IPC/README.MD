## (Was a) Part of [MirrOx](https://github.com/IDKSAM27/MirrOx)


More info in [MirrOx/notes](https://github.com/IDKSAM27/MirrOx/blob/main/doc_stuff/notes.txt) (somewhere around `15/04/2025`)

# jni

The **`jni`** project provides native C code for interacting with Android's low-level **Binder IPC mechanism** via JNI. It's designed to experiment with or extend the capabilities of the `MediaProjection` system service, enabling the manual construction of Binder transactions to request screen capture permissions or retrieve media projection tokens.

This is a low-level project that bypasses traditional Android SDK abstractions and directly interfaces with the `/dev/binder` device using native system calls and Binder protocol structures.

---

##  Features

-  JNI bridge for Android native-to-Java communication
-  Direct access to Android's `MediaProjection` service via Binder IPC
-  Binder transaction construction and parsing
-  Uses native shared library built via `Android.mk`
-  Foundation for custom Android system service interactions

---

##  Build Instructions

### Requirements

- Android NDK installed
- Android.mk-compatible build system (e.g., `ndk-build`, part of Android Studio NDK integration)

### Build with ndk-build

```bash
ndk-build NDK_PROJECT_PATH=. APP_BUILD_SCRIPT=./Android.mk
```


##  Overview

### JNI Integration

The native function declared in `media_projection.c`:

```c
JNIEXPORT jobject JNICALL Java_com_mirrox_server_StartMirrox_getMediaProjectionTokenNative(JNIEnv *env, jclass clazz);
```

...is intended to bridge Java code with low-level Binder IPC functionality, allowing advanced users to bypass Android's permission system (for research or rooted device use cases).

### Binder IPC

Binder structures and protocol constants (e.g., `BR_TRANSACTION`, `BC_TRANSACTION`) are manually defined. The project allows:

- Opening the `/dev/binder` device  
- Manually constructing a `binder_transaction_data` payload  
- Sending a custom transaction (e.g., to `IMediaProjectionManager.createProjection()`)

>  Note: Binder transactions require elevated privileges (e.g., root access) and detailed knowledge of the Binder ABI and service interfaces.

---

##  Work in Progress (Sadly aborted)

- The actual binder transaction logic (`send_create_projection_transaction`, `receive_media_projection_reply`) is declared but not yet implemented.  
-  Intended for experimentation or educational use only; not production-ready.  
-  Requires a rooted device or AOSP context to fully utilize.

---

##  Warning

This project uses undocumented and potentially unstable Android internals. **Use only in controlled, experimental, or research environments**. Improper use can result in system instability or undefined behavior.

---

##  License

MIT License – use at your own risk. Contributions and forks are welcome.

---

##  Contact

For issues, improvements, or questions, feel free to open a GitHub issue or contact [me](mailto:sampreetpatil@proton.me).
