/// SVG-style progress ring — mirrors vanilla's ringSvg(pct) (app.js
/// "Theory courses" section), drawn with a CustomPainter.
library;

import 'dart:math' as math;

import 'package:flutter/material.dart';

class CourseProgressRing extends StatelessWidget {
  final int pct;
  final double size;
  final double strokeWidth;

  const CourseProgressRing({
    super.key,
    required this.pct,
    this.size = 64,
    this.strokeWidth = 8,
  });

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    return Semantics(
      label: '$pct% complete',
      child: SizedBox(
        width: size,
        height: size,
        child: CustomPaint(
          painter: _RingPainter(
            pct: pct.clamp(0, 100),
            track: scheme.surfaceContainerHighest,
            bar: scheme.primary,
            strokeWidth: strokeWidth,
          ),
          child: Center(
            child: Text(
              '$pct%',
              style: Theme.of(context)
                  .textTheme
                  .labelMedium
                  ?.copyWith(fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ),
    );
  }
}

class _RingPainter extends CustomPainter {
  final int pct;
  final Color track;
  final Color bar;
  final double strokeWidth;

  _RingPainter({
    required this.pct,
    required this.track,
    required this.bar,
    required this.strokeWidth,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final c = size.center(Offset.zero);
    final r = (math.min(size.width, size.height) - strokeWidth) / 2;
    final trackPaint = Paint()
      ..color = track
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth;
    final barPaint = Paint()
      ..color = bar
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(c, r, trackPaint);
    const start = -math.pi / 2;
    canvas.drawArc(
      Rect.fromCircle(center: c, radius: r),
      start,
      (pct / 100) * 2 * math.pi,
      false,
      barPaint,
    );
  }

  @override
  bool shouldRepaint(covariant _RingPainter old) =>
      old.pct != pct || old.track != track || old.bar != bar;
}
