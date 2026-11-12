plugins {
    id("com.android.application")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

android {
    namespace = "com.raviyadav.loksewa_vidyapeeth"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    // Release signing: reads ENVIRONMENT variables when present
    // (KEYSTORE_PATH, KEYSTORE_PASSWORD, KEY_ALIAS, KEY_PASSWORD).
    // In CI these come from GitHub Actions secrets (the keystore itself is
    // decoded from ANDROID_KEYSTORE_BASE64 by the workflow — see
    // .github/workflows/flutter-release.yml). Locally, export them in your
    // shell before `flutter build apk --release` / `appbundle --release`
    // (see flutter/README.md). No key.properties file is used anymore.
    // When the env vars are absent, the release build falls back to the
    // debug keystore so `flutter run --release` and local dev builds keep
    // working everywhere.
    val releaseKeystorePath = System.getenv("KEYSTORE_PATH")
    val releaseKeystorePassword = System.getenv("KEYSTORE_PASSWORD")
    val releaseKeyAlias = System.getenv("KEY_ALIAS")
    val releaseKeyPassword = System.getenv("KEY_PASSWORD")
    val hasReleaseSigning = !releaseKeystorePath.isNullOrBlank() &&
        !releaseKeystorePassword.isNullOrBlank() &&
        !releaseKeyAlias.isNullOrBlank() &&
        !releaseKeyPassword.isNullOrBlank()

    defaultConfig {
        // TODO: Specify your own unique Application ID (https://developer.android.com/studio/build/application-id.html).
        applicationId = "com.raviyadav.loksewa_vidyapeeth"
        // You can update the following values to match your application needs.
        // For more information, see: https://flutter.dev/to/review-gradle-config.
        minSdk = flutter.minSdkVersion
        targetSdk = flutter.targetSdkVersion
        // Uses the version code from pubspec.yaml. When using split APKs, 1000 * ABI_VERSION
        // is added automatically by Flutter. (https://developer.android.com/studio/build/configure-apk-splits#configure-APK-versions)
        // You can force using the value of versionCode by specifying the `-P force-version-code-ignoring-abi=true`
        // flag during build.
        versionCode = flutter.versionCode
        versionName = flutter.versionName
    }

    signingConfigs {
        create("release") {
            // Re-read into locals so Kotlin smart-casts the null checks
            // below (a separate Boolean flag would not smart-cast).
            val storePath = releaseKeystorePath
            val storePass = releaseKeystorePassword
            val aliasValue = releaseKeyAlias
            val keyPass = releaseKeyPassword
            if (!storePath.isNullOrBlank() && !storePass.isNullOrBlank() &&
                !aliasValue.isNullOrBlank() && !keyPass.isNullOrBlank()
            ) {
                keyAlias = aliasValue
                keyPassword = keyPass
                storeFile = rootProject.file(storePath)
                storePassword = storePass
            }
        }
    }

    buildTypes {
        release {
            signingConfig = if (hasReleaseSigning) {
                signingConfigs.getByName("release")
            } else {
                // No signing env vars (local dev / fresh clone): debug keys
                // so `flutter run --release` and debug APK builds keep
                // working. CI fails fast instead of shipping a
                // debug-signed "release" — see flutter-release.yml.
                signingConfigs.getByName("debug")
            }
        }
    }
}

kotlin {
    compilerOptions {
        jvmTarget = org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17
    }
}

flutter {
    source = "../.."
}
