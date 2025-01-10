PRESERVED_SENDERS = [
    'LinkedIn',
    'Vagas.com.br',
    'InfoJobs',
    'Gupy',
    'Catho',
    'Indeed',
    'GeekHunter',
    'Programathor',
    'Revelo',
    'Glassdoor',
    'Trampos',
    'Workana',
    'RocketContent',
    'Stack Overflow',
    'GitHub',
    'Dev.to',
    'Burh',
    'Microsoft',
    'Riot Games',
    
]

# Função para verificar se um remetente deve ser preservado
def should_preserve_sender(sender_name):
    return any(preserved.lower() in sender_name.lower() for preserved in PRESERVED_SENDERS) 