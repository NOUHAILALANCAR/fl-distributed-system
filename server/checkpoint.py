import torch


def save_checkpoint(model, round_number):

    torch.save({

        "round": round_number,
        "model": model.state_dict()

    }, f"checkpoint_round_{round_number}.pth")
