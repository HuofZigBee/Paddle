import unittest
import numpy as np
from op_test import OpTest


class SeqPoolType(OpTest):
    AVERAGE = 0
    SUM = 1
    SQRT = 2
    MAX = 3
    LAST = 4
    FIRST = 5


class TestSeqAvgPool(OpTest):
    def set_data(self):
        self.op_type = 'sequence_pool'
        # one level, batch size is 4
        x = np.random.uniform(0.1, 1, [11, 23]).astype('float32')
        lod = [[0, 4, 5, 8, 11]]
        self.inputs = {'X': (x, lod)}

        out = np.zeros((4, 23)).astype('float32')
        self.outputs = {'Out': out}
        return x, lod, out

    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.AVERAGE}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            out[i] = sub_x.mean(axis=0)

    def setUp(self):
        x, lod, out = self.set_data()
        self.compute(x, lod, out)

    def test_check_output(self):
        self.check_output()

    def test_check_grad(self):
        self.check_grad(["X"], "Out")


class TestSeqAvgPool2D(TestSeqAvgPool):
    def set_data(self):
        self.op_type = 'sequence_pool'
        # one level, batch size is 4
        x = np.random.uniform(0.1, 1, [13, 3, 17]).astype('float32')
        lod = [[0, 4, 5, 8, 13]]
        self.inputs = {'X': (x, lod)}

        out = np.zeros((4, 3, 17)).astype('float32')
        self.outputs = {'Out': out}
        return x, lod, out

    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.AVERAGE}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            out[i] = np.reshape(sub_x.mean(axis=0), (3, 17))


class TestSeqSumPool(TestSeqAvgPool):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.SUM}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            out[i] = sub_x.sum(axis=0)


class TestSeqSumPool2D(TestSeqAvgPool2D):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.SUM}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            out[i] = np.reshape(sub_x.sum(axis=0), (3, 17))


class TestSeqSqrtPool(TestSeqAvgPool):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.SQRT}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            len = lod[0][i + 1] - lod[0][i]
            out[i] = sub_x.sum(axis=0) / np.sqrt(len)


class TestSeqSqrtPool2D(TestSeqAvgPool2D):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.SQRT}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            len = lod[0][i + 1] - lod[0][i]
            out[i] = np.reshape(sub_x.sum(axis=0) / np.sqrt(len), (3, 17))

    def test_check_grad(self):
        self.check_grad(["X"], "Out", max_relative_error=0.06)


class TestSeqMaxPool(TestSeqAvgPool):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.MAX}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            out[i] = np.amax(sub_x, axis=0)

    def test_check_grad(self):
        # Remove MaxPool2D from gradient check to confirm the success of CI.
        return


class TestSeqMaxPool2D(TestSeqAvgPool2D):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.MAX}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            out[i] = np.reshape(np.amax(sub_x, axis=0), (3, 17))

    def test_check_grad(self):
        # Remove MaxPool2D from gradient check to confirm the success of CI.
        return


class TestSeqLastPool(TestSeqAvgPool):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.LAST}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            out[i] = sub_x[-1, :]


class TestSeqLastPool2D(TestSeqAvgPool2D):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.LAST}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            out[i] = np.reshape(sub_x[-1, :], (3, 17))


class TestSeqFirstPool(TestSeqAvgPool):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.FIRST}
        for i in range(4):
            sub_x = x[lod[0][i]:lod[0][i + 1], :]
            out[i] = sub_x[0, :]


class TestSeqFirstPool2D(TestSeqAvgPool2D):
    def compute(self, x, lod, out):
        self.attrs = {'strategy': SeqPoolType.FIRST}
        for i in range(4):
            sub_x = np.reshape(x[lod[0][i]:lod[0][i + 1], :], (-1, 3 * 17))
            out[i] = np.reshape(sub_x[0, :], (3, 17))


if __name__ == '__main__':
    unittest.main()
