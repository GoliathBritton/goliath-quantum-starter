import os
from nqba import create_framework
from nqba.core.intelligence import qdllm, qnlp, qtransformers
# Temporarily disable Dynex integration due to import issues
# from dynex import DynexRuntime
dynex_runtime = None
# dynex_runtime = DynexRuntime(api_key=os.environ.get("DYNEX_API_KEY"))
framework = create_framework(
    enable_qdllm=True,
    enable_qnlp=True,
    enable_qtransformers=True,
    governance_enabled=True,
    compliance_checks=True,
    accelerator=dynex_runtime
)

def deploy_data_service(raw_data, synthesis_params):
    # QNLP labels and cleans data
    labeled_data = qnlp.process(raw_data, mode='data_labeling')
    
    # qdLLM generates synthetic variants
    synth_data = qdllm.reason(labeled_data, uncertainty_threshold=0.3, context='edge_cases')
    
    # QTransformers diversifies dataset
    diverse_set = qtransformers.optimize(synth_data, sparse_attention=True)
    
    # NQBA spawns curation entity
    curation_ai = framework.spawn_business_entity(
        type='data_synthesizer',
        workflow='qnpl_label -> qdllm_synth -> qtransformers_diversify',
        data=diverse_set
    )
    
    # Output curated dataset
    curated = curation_ai.execute('generate_dataset', params={'niche': 'medical_imaging'})
    return curated  # E.g., {'dataset_size': '50K samples', 'quality_improvement': '20%'}

# Example for fraud data
raw = "Client transaction logs."
params = "Rare fraud scenarios."
result = deploy_data_service(raw, params)
print(result)