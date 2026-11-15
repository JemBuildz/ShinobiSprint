import 'package:authentication_repository/authentication_repository.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:super_dash/game_intro/game_intro.dart';
import 'package:super_dash/settings/settings_controller.dart';

class _MockSettingsController extends Mock implements SettingsController {}

class _MockAuthenticationRepository extends Mock
    implements AuthenticationRepository {}

void main() {
  group('ShinobiGameSelectionPage', () {
    late SettingsController settingsController;
    late AuthenticationRepository authenticationRepository;

    setUp(() {
      settingsController = _MockSettingsController();
      when(() => settingsController.muted).thenReturn(ValueNotifier(false));
      authenticationRepository = _MockAuthenticationRepository();
    });

    Widget buildSubject() {
      return MultiRepositoryProvider(
        providers: [
          RepositoryProvider<SettingsController>.value(
            value: settingsController,
          ),
          RepositoryProvider<AuthenticationRepository>.value(
            value: authenticationRepository,
          ),
        ],
        child: const MaterialApp(
          home: ShinobiGameSelectionPage(),
        ),
      );
    }

    testWidgets('renders brand title, stage select, start run and settings',
        (tester) async {
      await tester.pumpWidget(buildSubject());

      expect(find.text('START RUN • LEVEL 1'), findsOneWidget);
      expect(find.text('STAGE SELECT'), findsOneWidget);
      expect(find.text('RANKINGS'), findsOneWidget);
      expect(find.text('SETTINGS'), findsOneWidget);
      expect(find.text('LOTUS SHADOW CLAN'), findsOneWidget);
      expect(find.text('V1.4.2 • FLAME ENGINE'), findsOneWidget);
    });

    testWidgets('tapping settings toggles audio', (tester) async {
      await tester.pumpWidget(buildSubject());

      await tester.tap(find.text('SETTINGS'));
      await tester.pump();

      verify(() => settingsController.toggleMuted()).called(1);
    });
  });
}
