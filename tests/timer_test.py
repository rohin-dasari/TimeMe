import unittest
from timeme import Timer

EXPERIMENT_NAME = 'func_test'
@Timer(EXPERIMENT_NAME, trials=5, pbar=False)
def test():
    return


class Thing:
    @Timer('method_test', trials=5, pbar=True, parallelize=True)
    def do_something(self):
        return



class TimerTest(unittest.TestCase):
    
    def tearDown(self):
        Timer.clear_records()

    def test_record_data(self):
        """
        test to make sure data is recorded when
        the timeme argument is set to True
        """
        test()
        self.assertFalse(EXPERIMENT_NAME in Timer.records.keys())
        test(timeme=True)
        self.assertTrue(EXPERIMENT_NAME in Timer.records.keys())

    def test_override_defaults(self):
        """
        test to make sure values can be overriden to allow
        for users to temporarily modify test conditions on the fly
        """
        test(timeme=True, timeme_params={'name': 'update_func_test'})
        self.assertTrue('update_func_test' in Timer.records.keys())

    def test_trial_count(self):
        """
        test to make sure user specified number of trials are recorded
        """
        test(timeme=True)
        self.assertTrue(len(Timer.records[EXPERIMENT_NAME]['test'][-1].data),
                        5)

    def test_profile_toggle(self):
        """
        test to make sure that cProfile stats are generated when the profile
        arg is toggled to True
        """
        test(timeme=True, timeme_params={'profile': True})
        self.assertTrue(type(Timer.records[EXPERIMENT_NAME]['test'][-1]),
                        list)


if __name__ == '__main__':
    unittest.main()



