## Postgres setup

Requirements
- postgres >= 10.0
- ubuntu >= 16.04LTS


### Postgres Cluster Setup
Your Postgres Cluster is stored in `/etc/postgresql/<version>/<cluster-name>/`. For simplicify, lets assume our Postgres version is `10` and our Postgres cluster name is `main` (which happens to be the default).

#### pdAdmin
If you want to use __pgAdmin__, allow 0.0.0.0/0 so that the client can access the local server:
1. Add the line `host all all 0.0.0.0/0 md5` to the file `/etc/postgresql/10/main/pg_hba.conf`. 
2. Uncomment/edit the file `/etc/postgres/10/main/postgresql.conf` so that the following lines look like this: `listen_addresses='*'` & `port=5432`
3. You will login to pgAdmin with the super user, postgres. To do so, you will also need to change the password of this user (see __Postgres Roles__ below to see how to do this).

#### Resetting your Postgres Cluster
If something goes wrong with your cluster and you'd like to reset, you can use teh following commands to drop the Postgres cluster and recreate it. 
- Drop postgres cluster: `sudo pg_dropcluster 10 main`
- Create postgres cluster: `sudo pg_createcluster 10 main`

When you delete/drop your cluster, you will clear all data in those directories. This includes `/etc/postgresql/10/main/pg_hba.conf` and `/etc/postgresql/10/main/pg_hba.conf`


### Postgres Server
If you make any modifications to `pg_hba.conf` or `postgresql.conf`, restart your server to apply the changes.

Start server: `sudo /etc/init.d/postgresql start`
Restart server: `sudo /etc/init.d/postgresql restart`
Get status: `sudo /etc/init.d/postgresql status`

You can also check that your Postgres server is running on port 5432 with the command `netstat -nlp | grep 5432`.


### Postgres Roles
Upon installation, Postgres will come preconfigured with a *super user* called *postgres*. However, this user should only be used for admin purposes. When developing your application, create another role.

#### Change password of (super user) postgres
Switch users to the *postgres* user and change the password for the user:
```sh
sudo -u postgres psql #open psql with the postgres user
psq: "ALTER USER postgres WITH PASSWORD 'password';"
```

#### Create new roles
Creating new roles can only be done by a super user, or a user with the correct permissions to create roles. The user postgres is a super user, so use the `createuser` command with the super user, postgres. 
```sh
sudo -u postgres createuser <username>
```
See `createuser` [docs](https://www.postgresql.org/docs/10/static/app-createuser.html)


### Postgres databases
Database creations/deletions should be done with the super user, postgres:

Create db: `sudo -u postgres createdb -U postgres -E utf8 -O <username> -T template0 -e <db_name>`
See `createdb` [docs](https://www.postgresql.org/docs/10/static/app-createdb.html)

Drop db: `sudo -u postgres dropdb <db_name>`
see `dropdb` [docs](https://www.postgresql.org/docs/9.3/static/app-dropdb.html)
