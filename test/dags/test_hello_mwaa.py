from airflow.models import DagBag
import unittest
import os

class TestHelloMWAA(unittest.TestCase):

    def setUp(self):
        self.dagbag = DagBag(os.path.expanduser("/usr/local/airflow/dags"), include_examples=False)

    def test_dag_loaded(self):
        dag1 = self.dagbag.get_dag(dag_id='hello-mwaa')
        assert len(dag1.tasks) == 2

    def assertDagDictEqual(self,source,dag):
        assert dag.task_dict.keys() == source.keys()
        for task_id, downstream_list in source.items():
            assert dag.has_task(task_id)
            task = dag.get_task(task_id)
            assert task.downstream_task_ids == set(downstream_list)
    def test_dag(self):
        dag = self.dagbag.get_dag(dag_id='hello-mwaa')
        self.assertDagDictEqual({
          "hello_task": ["hello_custom_task"],
          "hello_custom_task": []
        },dag)

suite = unittest.TestLoader().loadTestsFromTestCase(TestHelloMWAA)
unittest.TextTestRunner(verbosity=2).run(suite)
