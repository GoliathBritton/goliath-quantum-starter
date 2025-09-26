const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  const initialSupply = ethers.parseEther("1000000"); // 1 million tokens
  const NQBAToken = await hre.ethers.getContractFactory("NQBAToken");
  const nqbaToken = await NQBAToken.deploy(initialSupply);

  console.log(`NQBAToken deployed to: ${nqbaToken.target}`);

  const MCPWrapper = await hre.ethers.getContractFactory("MCPWrapper");
  const mcpWrapper = await MCPWrapper.deploy(nqbaToken.target);

  console.log(`MCPWrapper deployed to: ${mcpWrapper.target}`);

  const minimumQuorum = ethers.parseEther("1000"); // e.g., 1000 tokens
  const votingPeriod = 86400; // 1 day in seconds
  const DAOGovernance = await hre.ethers.getContractFactory("DAOGovernance");
  const daoGovernance = await DAOGovernance.deploy(nqbaToken.target, minimumQuorum, votingPeriod, deployer.address);

  console.log(`DAOGovernance deployed to: ${daoGovernance.target}`);
  const PennyLaneWrapper = await hre.ethers.getContractFactory("PennyLaneWrapper");
  const pennyLaneWrapper = await PennyLaneWrapper.deploy(nqbaToken.target);
  console.log(`PennyLaneWrapper deployed to: ${pennyLaneWrapper.target}`);
  const AutoGenWrapper = await hre.ethers.getContractFactory("AutoGenWrapper");
  const autoGenWrapper = await AutoGenWrapper.deploy(nqbaToken.target);
  console.log(`AutoGenWrapper deployed to: ${autoGenWrapper.target}`);
  const AkashWrapper = await hre.ethers.getContractFactory("AkashWrapper");
  const akashWrapper = await AkashWrapper.deploy(nqbaToken.target);
  console.log(`AkashWrapper deployed to: ${akashWrapper.target}`);
  const BubbleWrapper = await hre.ethers.getContractFactory("BubbleWrapper");
  const bubbleWrapper = await BubbleWrapper.deploy(nqbaToken.target);
  console.log(`BubbleWrapper deployed to: ${bubbleWrapper.target}`);
  const MCPNFT = await hre.ethers.getContractFactory("MCPNFT");
  const mcpNFT = await MCPNFT.deploy();
  console.log(`MCPNFT deployed to: ${mcpNFT.target}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });