from requests import put, get, delete, post
from networkx.readwrite import json_graph
import json


class NDlibClient(object):

    def __init__(self, service_url):
        self.token = ""
        self.base = service_url

    def create_experiment(self):
        res = get('%s/api/Experiment' % self.base).json()
        self.token = res['token']

    def destroy_experiment(self):
        res = delete('%s/api/Experiment' % self.base, data={'token': self.token})
        return res.status_code

    def reset_experiment(self, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = put('%s/api/ExperimentStatus' % self.base, data={'token': self.token, 'models': models})
        return res.status_code

    def describe_experiment(self):
        res = post('%s/api/ExperimentStatus' % self.base, data={'token': self.token}).json()
        return res

    def list_available_diffusion_models(self):
        res = get('%s/api/Models' % self.base).json()['endpoints']
        names = [res[x]['name'] for x in res]
        return names

    def list_available_graph_generators(self):
        res = get('%s/api/Generators' % self.base).json()['endpoints']
        names = [res[x]['name'] for x in res]
        return names

    def list_available_real_network_resources(self):
        res = get('%s/api/Networks' % self.base).json()['networks']
        names = [res[x]['name'] for x in res]
        return names

    def load_graph(self, name):
        res = put('%s/api/Networks' % self.base, data={'name': name, 'token': self.token})
        return res.status_code

    def add_barabasi_albert_graph(self, n, m):
        res = put("%s/api/Generators/BarabasiAlbertGraph" % self.base, data={'n': n, 'm': m, 'token': self.token})
        return res.status_code

    def add_erdos_renyi_graph(self, n, p, directed=False):
        gr = put("%s/api/Generators/ERGraph" % self.base, data={'n': n, 'p': p, 'directed': directed, 'token': self.token})
        return gr.status_code

    def add_wats_strogatz_graph(self, n, k, p):
        gr = put("%s/api/Generators/WSGraph" % self.base, data={'n': n, 'k': k, 'p': p, 'token': self.token})
        return gr.status_code

    def destroy_graph(self):
        res = delete('%s/api/Networks' % self.base, data={'token': self.token})
        return res.status_code

    def add_threshold_model(self, infected, threshold=0):
        res = put('%s/api/Threshold' % self.base, data={'infected': infected, 'threshold': threshold, 'token': self.token})
        return res.status_code

    def add_profile_model(self, infected, profile=0):
        res = put('%s/api/Profile' % self.base, data={'infected': infected, 'profile': profile, 'token': self.token})
        return res.status_code

    def add_profile_threshold_model(self, infected, threshold=0, profile=0):
        res = put('%s/api/ProfileThreshold' % self.base, data={'infected': infected, 'threshold': threshold, 'profile': profile, 'token': self.token})
        return res.status_code

    def add_SI(self, infected, beta):
        res = put('%s/api/SI' % self.base, data={'infected': infected, 'beta': beta, 'token': self.token})
        return res.status_code

    def add_SIS(self, infected, beta, lbd):
        res = put('%s/api/SIS' % self.base, data={'infected': infected, 'beta': beta, 'lambda': lbd, 'token': self.token})
        return res.status_code

    def add_SIR(self, infected, beta, gamma):
        res = put('%s/api/SIR' % self.base, data={'infected': infected, 'beta': beta, 'gamma': gamma, 'token': self.token})
        return res.status_code

    def add_independent_cascades(self, infected):
        res = put('%s/api/IndependentCascades' % self.base, data={'infected': infected, 'token': self.token})
        return res.status_code

    def destroy_model(self, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = delete('%s/api/Models' % self.base, data={'models': models , 'token': self.token})
        return res.status_code

    def set_advanced_configuration(self, configuration, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = put('%s/api/Configure' % self.base, data={'status': configuration, 'models': models, 'token': self.token})
        return res.status_code

    def get_iteration(self, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = post('%s/api/Iteration' % self.base, data={'token': self.token, 'models': models}).json()
        return res

    def get_iteration_bunch(self, bunch, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = post('%s/api/IterationBunch' % self.base, data={'bunch': bunch, 'models': models, 'token': self.token}).json()
        return res

    def get_complete_run(self, models=[]):
        if len(models) == 0:
            models = ''
        else:
            models = ','.join(models)

        res = post('%s/api/CompleteRun' % self.base, data={'token': self.token, 'models': models}).json()
        return res

    def get_graph(self):
        res = post('%s/api/GetGraph' % self.base, data={'token': self.token}).json()
        try:
            graph = json_graph.loads(json.dumps(res))
            return graph
        except:
            return None

    def get_list_available_exploratories(self):
        res = get('%s/api/Exploratory' % self.base).json()['exploratory']
        names = [x['name'] for x in res]
        return names

    def load_exploratory(self, name):
        res = post('%s/api/Exploratory' % self.base, data={'exploratory': name, 'token': self.token})
        return res.status_code
