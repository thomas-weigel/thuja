import unittest
from itemstream import Itemstream
from score import global_score
from generator import Generator
from generator import keys
from collections import OrderedDict
import numpy as np

class TestGenerators(unittest.TestCase):
    def test_indexpoints(self):
        tuplestream = Itemstream(
            [{keys.rhythm: "h", "indx": .769}, {keys.rhythm: "h", "indx": 1.95}, {keys.rhythm: "w", "indx": 3.175},
             {keys.rhythm: "h", "indx": 5.54}, {keys.rhythm: "h", "indx": 6.67}, {keys.rhythm: "h", "indx": 8.0}]
        )
        pitches = Itemstream(sum([
            ['c1', 'c', 'c', 'd', 'c1', 'c', 'c', 'd'],
        ], []))
        pitches.notetype = 'pitch'

        g = Generator(
            streams=OrderedDict([
                (keys.instrument, Itemstream([1])),
                (keys.duration, Itemstream([.1])),
                ('rhy|indx', tuplestream),
                (keys.amplitude, Itemstream([1])),
                (keys.frequency, pitches)
            ]),
            pfields=[
                keys.instrument,
                keys.start_time,
                keys.duration,
                keys.amplitude,
                keys.frequency,
                'indx'
                ]
        )

        # global_score.reinit(None, [amps, pitches, tuplestream], note_limit=(len(pitches.values) * 2))
        g.gen_lines = [';sine\n', 'f 1 0 16384 10 1\n', ';saw', 'f 2 0 256 7 0 128 1 0 -1 128 0\n', ';pulse\n',
                       'f 3 0 256 7 1 128 1 0 -1 128 -1\n']
        g.generate_notes()
        score_string = g.generate_score_string()
        self.assertTrue(score_string is not None)
        # self.assertTrue(len(score_string.split('\n')) == 22)

    def test_basiccase(self):
        rhythms = Itemstream(['q'], 'sequence', tempo=[120, 60, 30])
        rhythms.notetype = 'rhythm'
        amps = Itemstream([1])
        pitches = Itemstream(sum([
            ['c4', 'c', 'c', 'd', 'c5', 'c', 'c', 'd'],
        ], []))
        pitches.notetype = 'pitch'

        g = Generator(
            streams=OrderedDict([
                (keys.instrument, Itemstream([1])),
                (keys.duration, Itemstream([.1])),
                (keys.rhythm, rhythms),
                (keys.amplitude, amps),
                (keys.frequency, pitches)
            ])
        )

        g.gen_lines = [';sine\n', 'f 1 0 16384 10 1\n', ';saw', 'f 2 0 256 7 0 128 1 0 -1 128 0\n', ';pulse\n',
                       'f 3 0 256 7 1 128 1 0 -1 128 -1\n']
        g.generate_notes()

        output = ""
        for x in range(len(g.gen_lines)):
            output += g.gen_lines[x]
        for x in range(len(g.notes)):
            output += g.notes[x]

        score = g.generate_score_string()
        self.assertTrue(score is not None)
        print len(score.split('\n'))
        self.assertTrue(len(score.split('\n')) == 22)

if __name__ == '__main__':
    unittest.main()