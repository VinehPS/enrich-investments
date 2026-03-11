import base64
import json
from googleapiclient import discovery

def limit_cost(event, context):
    pubsub_data = base64.b64decode(event['data']).decode('utf-8')
    notification = json.loads(pubsub_data)
    
    cost = notification.get('costAmount')
    budget = notification.get('budgetAmount')

    if cost and budget and cost >= budget:
        # Pega o ID do projeto atual automaticamente
        project_id = notification.get('costIntervalStart').split('/')[-1] if not 'PROJECT_ID' in globals() else PROJECT_ID
        
        billing = discovery.build('cloudbilling', 'v1')
        name = f'projects/{project_id}'
        
        # DESLIGA o billing do projeto
        billing.projects().updateBillingInfo(name=name, body={'billingAccountName': ''}).execute()
        print(f"ALERTA: Faturamento desativado para o projeto {project_id} por atingir o limite.")
