const { expect } = require("chai");
const xrpl = require("xrpl");

describe("VeriHarvest XRPL Integration", function () {
  let client, wallet, destination;

  before(async function () {
    client = new xrpl.Client("wss://s.altnet.rippletest.net:51233");
    await client.connect();
    wallet = xrpl.Wallet.fromSeed("YOUR_ISSUER_SEED"); // Replace with actual seed
    destination = xrpl.Wallet.fromSeed("YOUR_DEST_SEED"); // Replace with actual seed
  });

  it("Should submit batch details to XRPL", async function () {
    const tx = {
      TransactionType: "Payment",
      Account: wallet.classicAddress,
      Destination: destination.classicAddress,
      Amount: {
        currency: "FRESH",
        issuer: wallet.classicAddress,
        value: "95",
      },
      Memos: [
        { Memo: { MemoData: Buffer.from("Organic Apples").toString("hex") } },
        { Memo: { MemoData: Buffer.from("Farm A").toString("hex") } },
        { Memo: { MemoData: Buffer.from("Safe").toString("hex") } },
      ],
    };

    const signedTx = await wallet.sign(tx);
    const response = await client.submitAndWait(signedTx.tx_blob);
    expect(response.result.engine_result).to.equal("tesSUCCESS");
  });

  after(async function () {
    await client.disconnect();
  });
});
