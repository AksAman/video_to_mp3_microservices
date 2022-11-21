const targetDbNames = ["videos", "mp3s"];
const rootUser = process.env.MONGO_INITDB_ROOT_USERNAME;
const rootPass = process.env.MONGO_INITDB_ROOT_PASSWORD;
const usersStr = process.env.MONGO_USERS_LIST;

const adminDb = db.getSiblingDB('admin');
adminDb.auth(rootUser, rootPass);
console.log('USER:SCRIPT:Successfully authenticated admin user');

console.log('USER:SCRIPT:usersStr', usersStr);

usersStr
    .trim()
    .split(';')
    .map(s => s.split(':'))
    .forEach(user => {
        const username = user[0];
        const rolesStr = user[1];
        const password = user[2];

        console.log("USER:SCRIPT:", username, rolesStr, password);

        if (!rolesStr || !password) {
            return;
        }

        const roles = rolesStr.split(',');
        const userDoc = {
            user: username,
            pwd: password,
            roles: []
        };

        roles.forEach(role => {
            targetDbNames.forEach(targetDbName => {
                userDoc.roles.push({
                    role: role,
                    db: targetDbName
                });
            });

            userDoc.roles.push({
                role: role,
                db: 'admin'
            });
        });

        console.log('USER:SCRIPT:Creating user', userDoc);

        targetDbNames.forEach(targetDbName => {
            const targetDb = db.getSiblingDB(targetDbName);
            try {
                targetDb.createUser(userDoc);
                console.log('USER:SCRIPT:Successfully created user', userDoc);
            } catch (err) {
                if (!~err.message.toLowerCase().indexOf('duplicate')) {
                    console.error("USER:SCRIPT:Error creating user", err);
                }
            }
        });

    });