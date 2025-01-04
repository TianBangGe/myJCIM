import torch
import pandas as pd

from data_utils import SolvDataset, set_seed
from train import train_model
from evaluate import (
    eval_model,
    process_dataset,
    process_dataset_ea
)


def main():
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    set_seed(0)

    # Load data from CSV
    df = pd.read_csv("resolved.csv")

    # Filtering out unstable molecules
    df = df.loc[df["stable"] == "stable"]
    df = df.loc[df["same_sml"] != "mwt_diff"]

    # Filter out problematic SMILES
    problem_smiles = [
        'C#CCC12CC(O1)c1c2nc(=N)sc1Br',
        'N=c1sc(Br)c2c3c1CC1OC(=NCC2)C31',
        'N=c1cnc2[nH]c(=O)c(cc2Br)c(=N)cc[nH]1',
        'N=c1nc2c(c(Br)s1)OC1C3CC(O3)C1O2',
        'N=c1nc2c(c(Br)s1)OCC21CC2CC1O2',
        'N=C1C=Cc2cc(Br)c(oc2=N)C=CN=CO1',
        'Cc1cc(C#N)cc(C(F)(F)F)c(=N)n1',
        'Cc1ccc(N)c(=NO)c(=O)cc1C(F)(F)F',
        'Cc1nccc(O)nc(CC(F)(F)F)c(C)s1',
        'CCC(O)c1c(F)c(C#N)nc(C)c1NC=N',
        'Cc1cnc(=NCC(F)(F)F)c(N)c(O)c1N',
        'CCC(=O)Oc1c(Cl)cnc2c1C1CC2O1',
        'Cc1c(NCC(F)(F)F)c(=N)ncccc1=N',
        'CCNCc1c(C(F)(F)F)c(=O)[nH]nnc1=N',
        'CC(N)c1cc(F)nc(=N)n1CC(O)C(N)=O',
        'CC(N)(c1cc(N)nc(F)n1)C(N)(CN)CN',
        'Cc1occoc(=N)c(C(F)(F)F)c(C)c1C',
        'CCc1ncnc(C(F)(F)F)cc(C)c(O)[nH]1',
        'CC12OC(C#N)(c3c1cc(Cl)nc3O)C2O'
    ]
    df = df[~df.smiles.isin(problem_smiles)]

    # Build dataset
    dataset = SolvDataset(
        df["smiles"],
        df["EA"],
        df["RP_ACN"],
        df["RP_H2O"],
        df["RP_THF"],
        df["RP_DMSO"],
        df["RP_DMF"],
        device
    )

    # Train the model
    model, trainloader, validloader, testloader = eval_model(
        dataset=dataset,
        df=df,
        device=device
    )

    # Loading the best model for inference
    model.load_state_dict(torch.load(
        "weights/no_EA_model.pth", map_location=device, weights_only=True))
    model.eval()

    # Evaluate train, test, validation for solvent properties
    with torch.no_grad():
        process_dataset(model, trainloader, "train", device=device)
        process_dataset(model, validloader, "validation", device=device)
        process_dataset(model, testloader, "test", device=device)

        # Evaluate EA channel
        process_dataset_ea(model, trainloader, "train_ea", device=device)
        process_dataset_ea(model, validloader, "validation_ea", device=device)
        process_dataset_ea(model, testloader, "test_ea", device=device)


if __name__ == "__main__":
    main()
