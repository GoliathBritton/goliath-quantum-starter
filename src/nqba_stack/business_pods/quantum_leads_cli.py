import click
from nqba_stack.business_pods.quantum_lead_generator import generate_leads


@click.command()
@click.option("--n", default=50, help="Number of leads to generate")
@click.option("--out", default="quantum_buyer_intent_leads.csv", help="Output CSV file")
def quantum_leads(n, out):
    """Generate best-in-class quantum buyer intent business leads."""
    df = generate_leads(n)
    df.to_csv(out, index=False)
    click.secho(f"Generated {n} quantum buyer intent leads: {out}", fg="green")


# Add to CLI group in cli.py:
# cli.add_command(quantum_leads)
