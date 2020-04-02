#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lmdb.h"




int main(int argc, char* argv[]){
    
    int rc;
    MDB_env *env;
    MDB_dbi dbi;
    MDB_val key, data;
    MDB_txn *txn;
    MDB_cursor *cursor;
    char strKey[50];
    char strValue[50];
    
    char* pDataDir = 0;
    int count = 10;

    if(argc > 2){
        pDataDir = argv[1];
        count = atoi(argv[2]);
    }else{
        printf("./main [dataDir] [count]\n");
        return -1;
    }

    if(0 == pDataDir){
        printf("data directory is null!\n");
        return -1;
    }

    printf("lmdb version:%s\n",mdb_version(0, 0, 0));

    rc = mdb_env_create(&env);
    if(rc){
        printf("mdb_env_create error,detail:%s\n", mdb_strerror(rc));
        return -1;
    }
    
    rc = mdb_env_open(env, pDataDir, 0, 0);
    if(rc){
        printf("mdb_env_open error,detail:%s\n", mdb_strerror(rc));
        return -1;
    }
    
    rc = mdb_txn_begin(env, NULL, 0, &txn);
    if(rc){
        printf("mdb_txn_begin error,detail:%s\n", mdb_strerror(rc));
        return -1;
    }

    rc = mdb_dbi_open(txn, NULL, 0, &dbi);
    if(rc){
        printf("mdb_dbi_open error,detail:%s\n", mdb_strerror(rc));
        return -1;
    }
    
    sprintf(strKey, "%s", "key");
    sprintf(strValue, "%s", "value");

    key.mv_size = strlen(strKey)*sizeof(char);
    key.mv_data = strKey;
    data.mv_size = strlen(strValue)*sizeof(char);
    data.mv_data = strValue;

    rc = mdb_put(txn, dbi, &key, &data, 0);
    rc = mdb_txn_commit(txn);
    if (rc) {
        fprintf(stderr, "mdb_txn_commit: (%d) %s\n", rc, mdb_strerror(rc));
        goto leave;
    }
    rc = mdb_txn_begin(env, NULL, MDB_RDONLY, &txn);
    
    rc = mdb_cursor_open(txn, dbi, &cursor);
    
    while ((rc = mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0) {
        memset(strKey, 0, sizeof(strKey));
        memset(strValue, 0, sizeof(strValue));
        strncpy(strKey, (const char*)key.mv_data, (int)key.mv_size);
        strncpy(strValue, (const char*)data.mv_data, (int)data.mv_size);
        
        printf("key:%s, value:%s\n",strKey, strValue);

        if(--count == 0){
            break;
        }
    }
    mdb_cursor_close(cursor);
    mdb_txn_abort(txn);
leave:
    mdb_dbi_close(env, dbi);
    mdb_env_close(env);
    return 0;
}
