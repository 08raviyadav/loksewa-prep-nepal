/// Daily content selection — pure, deterministic, unit-testable.
///
/// The Daily Challenge and the Question of the Day are seeded from the
/// UTC calendar date, so every user gets the same set on the same day
/// (and the same challenge set as the vanilla site, which uses the same
/// SeededRandom sequence).
library;

import '../data/data_repository.dart';
import '../models/models.dart';
import 'analytics.dart';

/// The Daily Challenge set: 10 questions drawn from [all] by the vanilla
/// shuffle (sort by successive SeededRandom draws). Same seed → same set.
List<Question> pickDailyChallenge(List<Question> all, String seed) {
  final rand = SeededRandom(seed);
  final shuffled = all.toList()
    ..sort((a, b) => rand.next().compareTo(rand.next()));
  return shuffled.take(10).toList();
}

/// One deterministic question from [pool] for the given [seed].
/// The '-qotd' suffix keeps the QOTD independent of the Daily Challenge
/// set (a different draw sequence from the same day seed).
Question? pickQuestionOfTheDay(List<Question> pool, String seed) {
  if (pool.isEmpty) return null;
  final rand = SeededRandom('$seed-qotd');
  return pool[(rand.next() * pool.length).floor()];
}

/// Loads today's Question of the Day.
///
/// Loading the whole 64k bank just to show one card would be slow, so
/// the file is picked deterministically by date (seed hash mod file
/// count) and only that one file is parsed. The file rotates day to day,
/// so the QOTD still ranges over the whole bank across the year.
Future<Question?> loadQuestionOfTheDay(
  DataRepository repo, {
  DateTime? now,
}) async {
  final seed = dailySeed(now);
  final idx = await repo.questionIndex();
  final files = idx['files'] as List;
  if (files.isEmpty) return null;
  final fileNo = seedHash(seed) % files.length;
  final name = (files[fileNo] as Map<String, dynamic>)['file'] as String;
  final qs = await repo.questions(name);
  return pickQuestionOfTheDay(qs, seed);
}
