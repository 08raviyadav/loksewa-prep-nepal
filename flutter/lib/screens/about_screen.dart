/// About this app (v1.0.2) — version, credits, data sources and links.
///
/// Reached from the drawer. Version comes from package_info_plus (the
/// pubspec version), so it is always the installed build's real number.
library;

import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:url_launcher/url_launcher.dart';

import '../data/data_repository.dart';
import '../theme/app_theme.dart';
import '../widgets/app_scaffold.dart';

class AboutScreen extends StatefulWidget {
  static const routeName = '/about';

  final int navIndex;
  final ValueChanged<int> onNav;

  const AboutScreen({super.key, required this.navIndex, required this.onNav});

  @override
  State<AboutScreen> createState() => _AboutScreenState();
}

class _AboutScreenState extends State<AboutScreen> {
  String? _version;
  late final Future<(int, int)> _statsFuture;

  @override
  void initState() {
    super.initState();
    _statsFuture = _loadStats();
    // Version is best-effort: if the platform lookup fails (e.g. in a
    // test without a mock), the screen still renders without it.
    PackageInfo.fromPlatform().then(
      (info) {
        if (mounted) {
          setState(() => _version = '${info.version} (${info.buildNumber})');
        }
      },
      onError: (_) {},
    );
  }

  Future<(int, int)> _loadStats() async {
    final repo = DataRepository();
    final exams = await repo.exams();
    final dates = await repo.examDates();
    return (exams.length, dates.length);
  }

  Future<void> _openLink(String url) async {
    final ok = await launchUrl(
      Uri.parse(url),
      mode: LaunchMode.externalApplication,
    );
    if (!ok && mounted) {
      final s = AppStateScope.of(context).strings;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(s.openLinkFailed)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final state = AppStateScope.of(context);
    final s = state.strings;
    return AppScaffold(
      title: s.aboutTitle,
      currentIndex: widget.navIndex,
      onNav: widget.onNav,
      body: ListView(
        padding: const EdgeInsets.all(AppSpacing.s4),
        children: [
          Center(
            child: Column(
              children: [
                Container(
                  width: 72,
                  height: 72,
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: AppColors.of(context).accent,
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    'O',
                    style: AppType.h1.copyWith(color: AppColors.of(context).accentInk),
                  ),
                ),
                const SizedBox(height: AppSpacing.s3),
                const Text('Outrank', style: AppType.h2),
                if (_version != null)
                  Text(
                    '${s.versionLabel} $_version',
                    style: AppType.small.copyWith(color: AppColors.of(context).muted),
                  ),
                const SizedBox(height: AppSpacing.s2),
                Text(
                  s.aboutTagline,
                  style: AppType.body.copyWith(color: AppColors.of(context).muted),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: AppSpacing.s2),
                Text(
                  s.madeInNepal,
                  style: AppType.small.copyWith(
                    color: AppColors.of(context).accent,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: AppSpacing.s4),
          FutureBuilder<(int, int)>(
            future: _statsFuture,
            builder: (context, snap) {
              if (!snap.hasData) return const SizedBox.shrink();
              final (examCount, dateCount) = snap.data!;
              return Row(
                children: [
                  Expanded(
                    child: _StatBox(value: '$examCount', label: s.examsLabel),
                  ),
                  const SizedBox(width: AppSpacing.s3),
                  Expanded(
                    child: _StatBox(value: '$dateCount', label: s.examDates),
                  ),
                ],
              );
            },
          ),
          const SizedBox(height: AppSpacing.s4),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.public_outlined),
            title: const Text('raviyadav.com.np'),
            subtitle: Text(s.websiteTitle),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openLink('https://raviyadav.com.np'),
          ),
          ListTile(
            leading: const Icon(Icons.code_outlined),
            title: const Text('github.com/08raviyadav/loksewa-prep-nepal'),
            subtitle: Text(s.footerCredit),
            trailing: const Icon(Icons.open_in_new, size: 18),
            onTap: () => _openLink(
              'https://github.com/08raviyadav/loksewa-prep-nepal',
            ),
          ),
          ListTile(
            leading: const Icon(Icons.description_outlined),
            title: Text(s.openSourceLicences),
            onTap: () => showLicensePage(
              context: context,
              applicationName: 'Outrank',
              applicationVersion: _version,
            ),
          ),
          const Divider(),
          const SizedBox(height: AppSpacing.s3),
          Text(s.dataSourcesTitle, style: AppType.h3),
          const SizedBox(height: AppSpacing.s2),
          Text(s.dataSourcesBody, style: AppType.body),
          const SizedBox(height: AppSpacing.s4),
          Center(
            child: Text(
              s.footerCredit,
              style: AppType.small.copyWith(color: AppColors.of(context).muted),
            ),
          ),
        ],
      ),
    );
  }
}

class _StatBox extends StatelessWidget {
  final String value;
  final String label;
  const _StatBox({required this.value, required this.label});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: AppSpacing.s3),
      decoration: BoxDecoration(
        color: AppColors.of(context).accentSoft,
        borderRadius: AppRadius.mdAll,
        border: Border.all(color: AppColors.of(context).accentLine),
      ),
      child: Column(
        children: [
          Text(value, style: AppType.h2.copyWith(color: AppColors.of(context).accent)),
          Text(label, style: AppType.small.copyWith(color: AppColors.of(context).muted)),
        ],
      ),
    );
  }
}
