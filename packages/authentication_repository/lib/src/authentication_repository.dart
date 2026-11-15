import 'dart:async';

import 'package:authentication_repository/authentication_repository.dart';
import 'package:firebase_auth/firebase_auth.dart' as fb;
import 'package:google_sign_in/google_sign_in.dart';
import 'package:sign_in_with_apple/sign_in_with_apple.dart';

/// {@template authentication_exception}
/// Exception thrown when an authentication process fails.
/// {@endtemplate}
class AuthenticationException implements Exception {
  /// {@macro authentication_exception}
  const AuthenticationException(this.error, this.stackTrace);

  /// The error that was caught.
  final Object error;

  /// The stack trace associated with the error.
  final StackTrace stackTrace;
}

/// {@template authentication_repository}
/// Repository to manage authentication.
/// {@endtemplate}
class AuthenticationRepository {
  /// {@macro authentication_repository}
  AuthenticationRepository({
    fb.FirebaseAuth? firebaseAuth,
  })  : _firebaseAuth = firebaseAuth ?? fb.FirebaseAuth.instance,
        _userController = StreamController<User>.broadcast();

  final fb.FirebaseAuth _firebaseAuth;
  final StreamController<User> _userController;
  StreamSubscription<fb.User?>? _firebaseUserSubscription;

  /// Stream of [User] which will emit the current user when
  /// the authentication state changes.
  ///
  /// Emits [User.unauthenticated] if the user is not authenticated.
  Stream<User> get user {
    _firebaseUserSubscription ??=
        _firebaseAuth.authStateChanges().listen((firebaseUser) {
      _userController.add(
        firebaseUser?.toUser ?? User.unauthenticated,
      );
    });

    return _userController.stream;
  }

  /// Stream of id tokens that can be used to authenticate with Firebase.
  Stream<String?> get idToken {
    return _firebaseAuth
        .idTokenChanges()
        .asyncMap((user) => user?.getIdToken());
  }

  /// Refreshes the id token.
  Future<String?> refreshIdToken() async {
    final user = _firebaseAuth.currentUser;
    return user?.getIdToken(true);
  }

  /// Sign in the user anonymously.
  ///
  /// If the sign in fails, an [AuthenticationException] is thrown.
  Future<void> signInAnonymously() async {
    try {
      final userCredential = await _firebaseAuth.signInAnonymously();
      _userController.add(userCredential.toUser);
    } on Exception catch (error, stackTrace) {
      throw AuthenticationException(error, stackTrace);
    }
  }

  /// Sign in the user with Google.
  ///
  /// If the sign in fails or is cancelled, an [AuthenticationException] is thrown.
  Future<void> signInWithGoogle({GoogleSignIn? googleSignIn}) async {
    try {
      final googleSignInInstance = googleSignIn ?? GoogleSignIn();
      final googleUser = await googleSignInInstance.signIn();
      if (googleUser == null) {
        throw const AuthenticationException(
          'Google sign-in was cancelled by the user.',
          StackTrace.empty,
        );
      }
      final googleAuth = await googleUser.authentication;
      final credential = fb.GoogleAuthProvider.credential(
        accessToken: googleAuth.accessToken,
        idToken: googleAuth.idToken,
      );
      final userCredential =
          await _firebaseAuth.signInWithCredential(credential);
      _userController.add(userCredential.toUser);
    } on Exception catch (error, stackTrace) {
      throw AuthenticationException(error, stackTrace);
    }
  }

  /// Sign in the user with Apple.
  ///
  /// If the sign in fails or is cancelled, an [AuthenticationException] is thrown.
  Future<void> signInWithApple({
    Future<fb.UserCredential> Function()? customAppleSignIn,
  }) async {
    try {
      if (customAppleSignIn != null) {
        final userCredential = await customAppleSignIn();
        _userController.add(userCredential.toUser);
        return;
      }
      final appleCredential = await SignInWithApple.getAppleIDCredential(
        scopes: [
          AppleIDAuthorizationScopes.email,
          AppleIDAuthorizationScopes.fullName,
        ],
      );
      final oauthCredential = fb.OAuthProvider('apple.com').credential(
        idToken: appleCredential.identityToken,
        accessToken: appleCredential.authorizationCode,
      );
      final userCredential =
          await _firebaseAuth.signInWithCredential(oauthCredential);
      _userController.add(userCredential.toUser);
    } on Exception catch (error, stackTrace) {
      throw AuthenticationException(error, stackTrace);
    }
  }

  /// Sign in the user with email and password.
  ///
  /// If the sign in fails, an [AuthenticationException] is thrown.
  Future<void> signInWithEmailAndPassword({
    required String email,
    required String password,
  }) async {
    try {
      final userCredential = await _firebaseAuth.signInWithEmailAndPassword(
        email: email,
        password: password,
      );
      _userController.add(userCredential.toUser);
    } on Exception catch (error, stackTrace) {
      throw AuthenticationException(error, stackTrace);
    }
  }

  /// Signs out the current user.
  Future<void> signOut() async {
    try {
      await _firebaseAuth.signOut();
      _userController.add(User.unauthenticated);
    } on Exception catch (error, stackTrace) {
      throw AuthenticationException(error, stackTrace);
    }
  }

  /// Disposes any internal resources.
  void dispose() {
    _firebaseUserSubscription?.cancel();
    _userController.close();
  }
}

extension on fb.User {
  User get toUser => User(id: uid);
}

extension on fb.UserCredential {
  User get toUser => user?.toUser ?? User.unauthenticated;
}
