import torch
import torch.nn.functional as F

from . import FFNet
from ..utils import gumbel_softmax_sample, normal_sample


class ZNet(torch.nn.Module):

    def __init__(self, config, z_type):
        super(ZNet, self).__init__()
        self.config = config
        self.z_type = z_type
        z_input_size = config['input_encoder_hidden_size'] *\
                       (1 + int(config['bidirectional_encoder'])) +\
                       config['vrnn_hidden_size']
        self.posterior_net1 = FFNet(z_input_size,
                                    config['posterior_ff_sizes1'],
                                    drop_prob=config['drop_prob'])
        if self.z_type == 'gumbel':
            # self.posterior_projection = torch.nn.Linear(config['posterior_ff_sizes1'][-1], config['z_logits_dim'])
            self.posterior_projection = torch.nn.Linear(z_input_size, config['z_logits_dim'])
        else:
            # self.posterior_projection = torch.nn.Linear(config['posterior_ff_sizes1'][-1], config['z_logits_dim'] * 2)
            self.posterior_projection = torch.nn.Linear(z_input_size, config['z_logits_dim'] * 2)
        self.posterior_net2 = FFNet(config['z_logits_dim'],
                                    config['posterior_ff_sizes2'],
                                    drop_prob=config['drop_prob'])

        self.prior_net = FFNet(config['z_logits_dim'], config['prior_ff_sizes'], drop_prob=config['drop_prob'])
        self.prior_projection = torch.nn.Linear(config['prior_ff_sizes'][-1], config['z_logits_dim'])

    def forward(self, x, z_previous):
        # x = self.posterior_net1(x)
        z_posterior_logits = self.posterior_projection(x)
        z_prior_logits = self.prior_net(z_previous)
        z_prior_logits = self.prior_projection(z_prior_logits)
        p_z = F.softmax(z_prior_logits, dim=-1)

        if self.z_type == 'gumbel':
            q_z = F.softmax(z_posterior_logits, dim=-1)
            q_z_samples, q_z_samples_logits =\
                gumbel_softmax_sample(z_posterior_logits, self.config['gumbel_softmax_tmp'])
        else:
            mu = z_posterior_logits[:, :self.config['z_logits_dim']]
            logvar = z_posterior_logits[:, self.config['z_logits_dim']:]
            q_z = z_posterior_logits
            q_z_samples = normal_sample(mu, logvar)
        p_z_samples, p_z_samples_logits =\
            gumbel_softmax_sample(z_prior_logits, self.config['gumbel_softmax_tmp'])
        # z_posterior_projection = self.posterior_net2(q_z_samples)

        return q_z_samples, q_z, p_z_samples, p_z
