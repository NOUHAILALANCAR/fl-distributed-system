import torch
import os
from common.model import get_model
from monitoring.logger import logger

CHECKPOINT_DIR = "checkpoints"

os.makedirs(CHECKPOINT_DIR, exist_ok=True)

def save_checkpoint(model, round_num):
    path = f"{CHECKPOINT_DIR}/model_round_{round_num}.pth"
    torch.save({
        'round': round_num,
        'model_state_dict': model.state_dict()
    }, path)
    logger.info(f"💾 Checkpoint saved: Round {round_num}")

def load_latest_checkpoint():
    if not os.path.exists(CHECKPOINT_DIR):
        return None
    
    files = [f for f in os.listdir(CHECKPOINT_DIR) if f.endswith('.pth')]
    if not files:
        return None
    
    latest = max(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    path = f"{CHECKPOINT_DIR}/{latest}"
    
    checkpoint = torch.load(path, weights_only=True, map_location='cpu')
    logger.info(f"🔄 Loaded checkpoint from round {checkpoint['round']}")
    return checkpoint
