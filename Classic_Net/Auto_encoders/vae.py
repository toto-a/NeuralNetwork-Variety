import torch
import torch.nn as nn
import torch.nn.functional as F

device=torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class VAE(nn.Module) :
    def __init__(self, in_features,hidden_dim=256,latent_features=200,type='linear',device=device) -> None:
        super().__init__()
        self.encoder=nn.Sequential(
            nn.Linear(in_features,hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim,latent_features),
            nn.LeakyReLU(0.2),
          
        )
        
        ## Latent features (mean and variance)
        self.fc_mu=nn.Linear(latent_features,2)
        self.fc_var=nn.Linear(latent_features,2)
        
        
        self.decoder=nn.Sequential(
            nn.Linear(2,latent_features),
            nn.LeakyReLU(0.2),
            nn.Linear(latent_features,hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim,in_features),
            nn.Sigmoid()
        )
        
        
    def encode(self,x):
        x=self.encoder(x)
        mu=self.fc_mu(x)
        log_var=self.fc_var(x)
        
        return mu,log_var
    
    
    def reparametrize(self,mu,log_var):

        ##Stochastic node
        epsilon=torch.randn_like(log_var).to(device)
        z=mu + log_var*epsilon
        
        return z
    
    
    def decode(self,z):
        return self.decoder(z)
    
    
    def forward(self,x) :
        mu,log_var=self.encode(x)
        z=self.reparametrize(mu,log_var)
        x_hat=self.decode(z)
        
        return x_hat,mu,log_var



