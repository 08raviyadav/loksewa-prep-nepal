import 'package:flutter/material.dart';

import '../theme/app_theme.dart';

/// Big-number stat card used by the dashboard stat grid
/// (mirrors the vanilla `#dash-stats .card .stat` cells).
class StatCard extends StatelessWidget {
  final String value;
  final String label;

  const StatCard({super.key, required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s3),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              value,
              style: AppType.h1,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: AppSpacing.s1),
            Text(label, style: AppType.small.copyWith(color: AppColors.of(context).muted)),
          ],
        ),
      ),
    );
  }
}

/// A labelled progress bar card (level progress, weekly goal).
class ProgressCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final double progress; // 0..1
  final Color? barColor;

  const ProgressCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.progress,
    this.barColor,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: EdgeInsets.zero,
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.s4),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(title, style: AppType.h3),
            const SizedBox(height: AppSpacing.s1),
            Text(
              subtitle,
              style: AppType.small.copyWith(color: AppColors.of(context).muted),
            ),
            const SizedBox(height: AppSpacing.s2),
            ClipRRect(
              borderRadius: AppRadius.smAll,
              child: LinearProgressIndicator(
                value: progress.clamp(0.0, 1.0),
                minHeight: 10,
                backgroundColor: AppColors.of(context).borderSoft,
                valueColor: AlwaysStoppedAnimation<Color>(
                  barColor ?? AppColors.of(context).accent,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
