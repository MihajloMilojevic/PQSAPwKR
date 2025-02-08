from . import base
from . import single_key
from . import utils

# Test use

# 1. commitment: string
# 2. shares : list of share objects {share, tag, commitment}
# 3. validation of the tags: boolean, requires the commitment and password
# 4. recovery: reversed of step 2
# 5. validation of the recovered key: 

# # generation

# generator = SingleKeyShareGenerator(t, p)
# generator.commit(secret)
# shares = generator.shares(password, n, start = 1)
# commitment = generator.commitment

# # validation

# validator = SingleKeyShareValidator(commitment)
# validator.validateShare(share, password)
# validator.validateSecret(secret)

# # recovery

# recoverer = SingleKeyShareRecoverer(t, p)
# secret = recoverer.recover(shares)

