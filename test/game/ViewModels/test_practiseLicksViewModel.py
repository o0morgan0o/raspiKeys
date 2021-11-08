import unittest
from src.game.ViewModels.practiseLicksViewModel import TranspositionMode, PractiseLicksViewModel


class TestGetNextTransposeOffset(unittest.TestCase):

    def testMinorSecondSequentialTransposeFromTranspose0(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 0
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose)
        self.assertEqual(result, 1)

    def testMinorSecondSequentialTransposeFromTranspose5(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 5
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose)
        self.assertEqual(result, 6)

    def testMinorSecondSequentialTransposeFromTranspose6(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 6
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose)
        self.assertEqual(result, -5)

    def testMinorThirdSequentialTransposeFromTranspose6(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 6
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose, 3)
        self.assertEqual(result, -3)

    def testMinorThirdSequentialTransposeFromTranspose7(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 7
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose, 3)
        self.assertEqual(result, -2)

    def testMajorThirdSequentialTransposeFromTranspose7(self):
        transpositionMode = TranspositionMode.TRANSPOSE_SEQUENTIAL.value
        current_transpose = 7
        result = PractiseLicksViewModel.getNextTransposeOffset(transpositionMode, current_transpose, 4)
        self.assertEqual(result, -1)
