#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <string>
#include "lmdb.h"
#include "common/MemoryStreams.hpp"
#include "seria/BinaryInputStream.hpp"
#include "seria/BinaryOutputStream.hpp"

typedef uint32_t Timestamp;
typedef uint64_t PeerIdType;

struct NetworkAddress {
    uint32_t ip   = 0;
    uint32_t port = 0;
};

struct PeerlistEntry {
     NetworkAddress adr;
     PeerIdType id      = 0;
     uint32_t last_seen = 0;  // coincides with Timestamp
     uint32_t reserved  = 0;  // High part of former 64-bit last_seen
};

struct Entry : public PeerlistEntry {
            Entry()
                : PeerlistEntry{}  // Initialize all fields
            {}
            Timestamp ban_until               = 0;
            Timestamp next_connection_attempt = 0;
            uint64_t shuffle_random = 0;  // We assign random number to  each record, for deterministic order of equal items
            std::string error;            // last ban reason
};


namespace seria {

void ser_members(PeerlistEntry &v, seria::ISeria &s) {
    seria_kv("adr", v.adr, s);
    seria_kv("id", v.id, s);
    seria_kv("last_seen", v.last_seen, s);
    //  uint64_t last_seen_64 = v.last_seen;
    //      //  seria_kv("last_seen", last_seen_64, s);
    //          //  if (s.is_input())
    //              //      v.last_seen = static_cast<uint32_t>(last_seen_64);
    //                  //  seria_kv("reserved", v.reserved, s);
}
void ser_members(Entry &v, ISeria &s) {
    ser_members(static_cast<PeerlistEntry &>(v), s);
    seria_kv("ban_until", v.ban_until, s);
    seria_kv("shuffle_random", v.shuffle_random, s);
    seria_kv("next_connection_attempt", v.next_connection_attempt, s);
    seria_kv("error", v.error, s);
}

void ser_members(NetworkAddress &v, seria::ISeria &s) {
    seria_kv("ip", v.ip, s);
    seria_kv("port", v.port, s);
}
}

struct Val {
    MDB_val impl{};

    Val() noexcept {}
    explicit Val(const std::string &data) noexcept : Val{data.data(), data.size()} {}
    Val(const void *const data, const std::size_t size) noexcept : impl{size, const_cast<void *>(data)} {}
    operator MDB_val *() noexcept { return &impl; }
    operator const MDB_val *() const noexcept { return &impl; }
    bool empty() const noexcept { return size() == 0; }
    std::size_t size() const noexcept { return impl.mv_size; }
    char *data() noexcept { return reinterpret_cast<char *>(impl.mv_data); }
    const char *data() const noexcept { return reinterpret_cast<char *>(impl.mv_data); }
};

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
    
    Entry entry;

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

    
    //rc = mdb_put(txn, dbi, &key, &data, 0);
    //rc = mdb_txn_commit(txn);
    //if (rc) {
    //    fprintf(stderr, "mdb_txn_commit: (%d) %s\n", rc, mdb_strerror(rc));
    //    return -1;
    //}
    

    //write peerDB
    entry.adr.ip = 10000;
    entry.adr.port = 8080;
    std::string peerKey = "/whitelist/1289242423:8080";
    common::BinaryArray value = seria::to_binary(entry);
    key.mv_size = peerKey.length();
    key.mv_data = (void*)peerKey.c_str();
    data.mv_size = value.size();
    data.mv_data = value.data();
    Val temp_value(value.data(), value.size());
    rc = ::mdb_put(txn, dbi, &key, &data, 0);
    if (rc != MDB_SUCCESS && rc != MDB_KEYEXIST){
        printf("write lmdb error!\n");
    }
    rc = mdb_txn_commit(txn);
    if (rc) {
        fprintf(stderr, "mdb_txn_commit: (%d) %s\n", rc, mdb_strerror(rc));
        return -1;
    }




    rc = mdb_txn_begin(env, NULL, MDB_RDONLY, &txn);
    
    rc = mdb_cursor_open(txn, dbi, &cursor);
    
    while ((rc = mdb_cursor_get(cursor, &key, &data, MDB_NEXT)) == 0) {
        
        memset(strKey, 0, sizeof(strKey));
        strncpy(strKey, (const char*)key.mv_data, (int)key.mv_size);
        //printf("key:%s\n", strKey);

        common::BinaryArray result = common::BinaryArray((char*)data.mv_data, (char*)data.mv_data + data.mv_size);
        
        Entry peer{};
        seria::from_binary(peer, result);

        
        printf("key:%s, value:Entry(adr.ip:%u,adr.port:%u,id:%lu,last_seen:%d,reserved:%d,ban_until:%d,next_connection_attempt:%d,shuffle_random:%lu,error:%s)\n",strKey, peer.adr.ip, peer.adr.port,peer.id,peer.last_seen,peer.reserved,peer.ban_until,peer.next_connection_attempt,peer.shuffle_random,peer.error.c_str());
        
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



