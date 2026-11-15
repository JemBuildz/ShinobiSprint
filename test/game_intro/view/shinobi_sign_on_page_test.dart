import 'package:authentication_repository/authentication_repository.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/settings/settings_controller.dart';

class _MockAuthenticationRepository extends Mock
    implements AuthenticationRepository {}

class _MockSettingsController extends Mock implements SettingsController {}

void main() {
  group('ShinobiSignOnPage', () {
    late AuthenticationRepository authenticationRepository;
    late SettingsController settingsController;

    setUp(() {
      authenticationRepository = _MockAuthenticationRepository();
      settingsController = _MockSettingsController();

      when(() => settingsController.muted).thenReturn(ValueNotifier(false));
      when(authenticationRepository.signInAnonymously).thenAnswer(
        (_) => Future.value(),
      );
      when(authenticationRepository.signInWithGoogle).thenAnswer(
        (_) => Future.value(),
      );
      when(authenticationRepository.signInWithApple).thenAnswer(
        (_) => Future.value(),
      );
    });

    Widget buildSubject() {
      return MultiRepositoryProvider(
        providers: [
          RepositoryProvider<AuthenticationRepository>.value(
            value: authenticationRepository,
          ),
          RepositoryProvider<SettingsController>.value(
            value: settingsController,
          ),
        ],
        child: const MaterialApp(
          home: ShinobiSignOnPage(),
        ),
      );
    }

    testWidgets('renders all sign-on options and buttons', (tester) async {
      await tester.pumpWidget(buildSubject());

      expect(find.text('Sign in with Google'), findsOneWidget);
      expect(find.text('Sign in with Apple'), findsOneWidget);
      expect(find.text('PLAY AS GUEST'), findsOneWidget);
      expect(
        find.text(
          "By continuing, you agree to Shinobi Sprint's Terms & Privacy",
        ),
        findsOneWidget,
      );
    });

    testWidgets('tapping PLAY AS GUEST signs in anonymously', (tester) async {
      await tester.pumpWidget(buildSubject());

      await tester.tap(find.text('PLAY AS GUEST'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump(const Duration(milliseconds: 500));

      verify(() => authenticationRepository.signInAnonymously()).called(1);
    });

    testWidgets('tapping Sign in with Google triggers signInWithGoogle',
        (tester) async {
      await tester.pumpWidget(buildSubject());

      await tester.tap(find.text('Sign in with Google'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump(const Duration(milliseconds: 500));

      verify(() => authenticationRepository.signInWithGoogle()).called(1);
    });

    testWidgets('tapping Sign in with Apple triggers signInWithApple',
        (tester) async {
      await tester.pumpWidget(buildSubject());

      await tester.tap(find.text('Sign in with Apple'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));
      await tester.pump(const Duration(milliseconds: 500));

      verify(() => authenticationRepository.signInWithApple()).called(1);
    });

    testWidgets('displays error snackbar when sign-in fails', (tester) async {
      when(authenticationRepository.signInWithGoogle).thenThrow(
        Exception('Network timeout'),
      );

      await tester.pumpWidget(buildSubject());

      await tester.tap(find.text('Sign in with Google'));
      await tester.pump();
      await tester.pump(const Duration(milliseconds: 500));

      expect(
        find.textContaining('Sign in notice: Exception: Network timeout'),
        findsOneWidget,
      );
    });
  });
}
