const localCache = new Map()

localCache.exists = key => localCache.has(key)
localCache.expire = (key, ttl) => setTimeout(() => localCache.delete(key), ttl * 1000)
localCache.on = (_, connection) => connection('🧶  No local Redis instance found... Defaulting to an in-memory cache storage.')

export default localCache
