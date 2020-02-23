
1. every ledger that is sent to a user id is encrypted with a key that maps onto their user id
2. ahead of time, 1000 very difficult blockchain hashes are precomputed and stored in local memory (2 for proof of concept)
3. the root node value of a randomly selected blockchain from disk is sent to a user attempting to receive the decryption key for a given uid.
4. the user must complete the hash and send the result to the server to have it checked.
5. if the hash they send matches the head node on that specific blockchain problem, then they are sent the decryption key that matches their user id.
6. now they're in the peer to peer network
