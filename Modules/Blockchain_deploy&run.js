
Write a test in test/veriharvest.test.js:

const { expect } = require("chai");

describe("VeriHarvest Contract", function () {
  let VeriHarvest, veriharvest, owner;

  beforeEach(async function () {
    [owner] = await ethers.getSigners();
    VeriHarvest = await ethers.getContractFactory("VeriHarvest");
    veriharvest = await VeriHarvest.deploy();
    await veriharvest.addBatch("Organic Apples", "Farm A", 95);
  });

  it("Should return correct batch details", async function () {
    const batch = await veriharvest.getBatchDetails(1);
    expect(batch.productName).to.equal("Organic Apples");
    expect(batch.status).to.equal("Safe");
  });

  it("Should update batch status", async function () {
    await veriharvest.updateBatchStatus(1, "Warning");
    const batch = await veriharvest.getBatchDetails(1);
    expect(batch.status).to.equal("Warning");
  });
});

Run the test:

npx hardhat test
