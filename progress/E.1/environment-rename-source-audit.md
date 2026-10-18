# Patch archive mapping revision — E.1

Candidate source for the authorized integration_test/E1_INTEGRATION and user_acceptance_test/E1_UAT rename. APEX/db remain byte-identical to the accepted 752eb47 Hello 1.0.1 source. The patch base points to the newly retained 1.0.0 mapping archive. Old archives are immutable. Native new-area identity checks and control compilation pass; mapping-boundary unit tests pass.

The prior immutable patch archive contains passed candidate evidence for the unchanged application/database behavior. The source equivalence and original evidence hashes are checked before reusing that result for this mapping-only candidate. This does not claim fresh integration/UAT qualification: F must qualify the new archive against empty and new 1.0.0 starts before promotion. Current C remains the preserved 1.0.0 development checkpoint; it is not upgraded merely to repackage unchanged application behavior. Final evidence lives in the main sprint audit. No push.
