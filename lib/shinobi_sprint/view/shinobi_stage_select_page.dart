import 'package:flutter/material.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_level.dart';
import 'package:super_dash/shinobi_sprint/models/shinobi_progress.dart';
import 'package:super_dash/shinobi_sprint/view/shinobi_stage_view.dart';

/// Full stage-selection menu for Shinobi Sprint showcasing all 3 Acts/Worlds
/// and their 15 handcrafted levels with 3-star progression and time trial
/// badges.
class ShinobiStageSelectPage extends StatefulWidget {
  const ShinobiStageSelectPage({super.key});

  static Route<void> route() {
    return MaterialPageRoute<void>(
      builder: (_) => const ShinobiStageSelectPage(),
    );
  }

  @override
  State<ShinobiStageSelectPage> createState() => _ShinobiStageSelectPageState();
}

class _ShinobiStageSelectPageState extends State<ShinobiStageSelectPage>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final progress = ShinobiProgressController.instance;

  @override
  void initState() {
    super.initState();
    _tabController =
        TabController(length: ShinobiWorld.values.length, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: progress,
      builder: (context, _) {
        final totalStars = progress.totalStars;

        return Scaffold(
          backgroundColor: const Color(0xFF090D16),
          appBar: AppBar(
            backgroundColor: Colors.transparent,
            elevation: 0,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.of(context).pop(),
            ),
            title: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(6),
                  decoration: BoxDecoration(
                    color: const Color(0xFF10B981).withValues(alpha: 0.2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(
                    Icons.sports_kabaddi,
                    color: Color(0xFF10B981),
                    size: 20,
                  ),
                ),
                const SizedBox(width: 10),
                const Text(
                  'SHINOBI SPRINT',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w900,
                    fontSize: 18,
                    letterSpacing: 1.2,
                  ),
                ),
                const Spacer(),
                // Total Stars Pill
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                  decoration: BoxDecoration(
                    color: const Color(0xFFFBBF24).withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(
                      color: const Color(0xFFFBBF24).withValues(alpha: 0.5),
                    ),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(
                        Icons.star_rounded,
                        color: Color(0xFFFBBF24),
                        size: 18,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        '$totalStars / ${ShinobiProgressController.maxCampaignStars}',
                        style: const TextStyle(
                          color: Color(0xFFFDE68A),
                          fontWeight: FontWeight.w900,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
            bottom: TabBar(
              controller: _tabController,
              indicatorColor: const Color(0xFF10B981),
              indicatorWeight: 3,
              labelColor: Colors.white,
              unselectedLabelColor: const Color(0xFF64748B),
              labelStyle: const TextStyle(
                fontWeight: FontWeight.w900,
                fontSize: 12,
                letterSpacing: 0.5,
              ),
              tabs: const [
                Tab(
                  icon: Icon(Icons.wb_sunny_outlined, size: 18),
                  text: 'ACT I: DAWN',
                ),
                Tab(
                  icon: Icon(Icons.wb_twilight_outlined, size: 18),
                  text: 'ACT II: TWILIGHT',
                ),
                Tab(
                  icon: Icon(Icons.nights_stay_outlined, size: 18),
                  text: 'ACT III: MIDNIGHT',
                ),
              ],
            ),
          ),
          body: TabBarView(
            controller: _tabController,
            children: ShinobiWorld.values.map(_buildWorldTab).toList(),
          ),
        );
      },
    );
  }

  Widget _buildWorldTab(ShinobiWorld world) {
    final levels = world.levels;

    return Center(
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: 820),
        child: ListView(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
          children: [
            // World Hero Card
            _buildWorldHero(world),

            const SizedBox(height: 16),

            // Section Header
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  '${world.title.toUpperCase()} • 5 LEVELS',
                  style: const TextStyle(
                    color: Color(0xFF64748B),
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 1,
                  ),
                ),
                Text(
                  world.timeOfDay,
                  style: TextStyle(
                    color: world.accentColor,
                    fontSize: 11,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),

            // 5 Level Cards
            ...levels.map(_buildLevelCard),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildWorldHero(ShinobiWorld world) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [
            world.themeColor.withValues(alpha: 0.35),
            const Color(0xFF0F172A),
          ],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(
          color: world.themeColor.withValues(alpha: 0.6),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: world.themeColor.withValues(alpha: 0.15),
            blurRadius: 16,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: world.themeColor.withValues(alpha: 0.25),
              shape: BoxShape.circle,
            ),
            child: Icon(
              world.icon,
              color: world.accentColor,
              size: 36,
            ),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  world.title.toUpperCase(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 17,
                    fontWeight: FontWeight.w900,
                    letterSpacing: 0.8,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  world.description,
                  style: const TextStyle(
                    color: Color(0xFF94A3B8),
                    fontSize: 12,
                    height: 1.3,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLevelCard(ShinobiLevel level) {
    final isUnlocked = progress.isLevelUnlocked(level.id);
    final starsEarned = progress.getStarsForLevel(level.id);

    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: isUnlocked
            ? const Color(0xFF131C2E)
            : const Color(0xFF0D131F).withValues(alpha: 0.6),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isUnlocked
              ? level.world.themeColor.withValues(alpha: 0.35)
              : Colors.white10,
        ),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: isUnlocked
              ? () {
                  Navigator.of(context).push(
                    ShinobiStageView.route(level: level),
                  );
                }
              : null,
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                // Level Number Badge
                Container(
                  width: 52,
                  height: 52,
                  decoration: BoxDecoration(
                    color: isUnlocked
                        ? level.world.themeColor.withValues(alpha: 0.2)
                        : Colors.white.withValues(alpha: 0.05),
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                      color: isUnlocked
                          ? level.world.themeColor.withValues(alpha: 0.6)
                          : Colors.white10,
                    ),
                  ),
                  child: Center(
                    child: Text(
                      level.id,
                      style: TextStyle(
                        color: isUnlocked ? Colors.white : Colors.white38,
                        fontWeight: FontWeight.w900,
                        fontSize: 16,
                      ),
                    ),
                  ),
                ),

                const SizedBox(width: 14),

                // Info Column
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          Expanded(
                            child: Text(
                              level.title,
                              style: TextStyle(
                                color:
                                    isUnlocked ? Colors.white : Colors.white38,
                                fontWeight: FontWeight.bold,
                                fontSize: 14,
                              ),
                              overflow: TextOverflow.ellipsis,
                            ),
                          ),
                          if (level.isTimeTrial) ...[
                            const SizedBox(width: 6),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 6,
                                vertical: 2,
                              ),
                              decoration: BoxDecoration(
                                color: Colors.amber.withValues(alpha: 0.2),
                                borderRadius: BorderRadius.circular(6),
                                border: Border.all(
                                  color: Colors.amber.withValues(alpha: 0.5),
                                ),
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  const Icon(
                                    Icons.timer,
                                    color: Colors.amber,
                                    size: 12,
                                  ),
                                  const SizedBox(width: 3),
                                  Text(
                                    '${level.timeLimit}s',
                                    style: const TextStyle(
                                      color: Colors.amber,
                                      fontSize: 10,
                                      fontWeight: FontWeight.w900,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(
                        level.description,
                        style: TextStyle(
                          color: isUnlocked
                              ? const Color(0xFF94A3B8)
                              : Colors.white24,
                          fontSize: 11,
                          height: 1.25,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 8),

                      // 3-Star Tracker
                      Row(
                        children: List.generate(3, (starIdx) {
                          final earned = starIdx < starsEarned;
                          return Padding(
                            padding: const EdgeInsets.only(right: 4),
                            child: Icon(
                              earned
                                  ? Icons.star_rounded
                                  : Icons.star_outline_rounded,
                              color: earned
                                  ? const Color(0xFFFBBF24)
                                  : isUnlocked
                                      ? Colors.white24
                                      : Colors.white10,
                              size: 18,
                            ),
                          );
                        }),
                      ),
                    ],
                  ),
                ),

                const SizedBox(width: 10),

                // Action Icon
                if (isUnlocked)
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: level.world.themeColor.withValues(alpha: 0.2),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      Icons.play_arrow_rounded,
                      color: level.world.accentColor,
                      size: 24,
                    ),
                  )
                else
                  const Icon(
                    Icons.lock_outline,
                    color: Colors.white24,
                    size: 22,
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
