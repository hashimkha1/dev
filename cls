[33mcommit 4dce60608b1f941f56411ff9d999f1a4143ef48e[m
Merge: f2e0a10 5ee406f
Author: Chris Maghas <coachofanalytics@gmail.com>
Date:   Thu Sep 1 14:08:33 2022 -0500

    Merge branch 'app-uat' of https://github.com/coachofanalytics/coda

[33mcommit 5ee406f7a10fa27ba4eb57e31117a440152617c7[m
Author: Chris Maghas <coachofanalytics@gmail.com>
Date:   Thu Sep 1 14:06:39 2022 -0500

    changes to accounts views: changed default value from 40 hours to 30 hours

[33mcommit 6691e3de92bf87273ab7178e40d07add2ed8227e[m
Merge: 7eb4966 e2d61f5
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 19:22:52 2022 +0530

    Merge branch 'coda_send_email_37120' into app-uat

[33mcommit e2d61f5ff593aa1c287ab115f5c9caa9c8ca6452[m
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 19:15:40 2022 +0530

    added a parse_mail() to parse data from gmail using googleapis and store them on CashappMail Models (the data needs to be cleaned)

[33mcommit 7eb496655af0546a4be4a59d7b71d20e8f0c82b8[m
Merge: b5f81ec 6d9e7ce
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 18:55:06 2022 +0530

    Merge branch 'coda_send_email_37121' into app-uat

[33mcommit 6d9e7ceed545630216746460e838c39b380e2f77[m
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 18:53:35 2022 +0530

    if the user is applicant the mail will be send via hr@codanalytics.net, added a separate email template to send mail.

[33mcommit 9cc553bd391c01ed6b2c3ddc8d3d0eb2161f58f5[m
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 18:33:31 2022 +0530

    added email settings based on environment variables.

[33mcommit dc8db5e7febeb42843458207138788834d6e9b72[m
Author: Pall Pandiyan <pallpandiyan.s@egrovesys.com>
Date:   Thu Sep 1 18:33:04 2022 +0530

    added python-dotenv package and loaded env on starting of the server. created a logger to log things.

[33mcommit e236ef3111f17a3274fdd42d14032d5e1fccb85a[m
Author: Sathishkumarvg <sathish@egrovesys.com>
Date:   Thu Sep 1 11:36:16 2022 +0530

    database add in dev_settings file

[33mcommit b5f81ec43e19827a2b227dcc32a9308532d63d89[m
Author: Chris Maghas <coachofanalytics@gmail.com>
Date:   Tue Aug 30 21:42:43 2022 -0500

    changes on data interview progress
