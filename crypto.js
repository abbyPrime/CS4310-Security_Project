const CryptoUtils = {
    async deriveKey(password, username) {
        const enc = new TextEncoder();
        const keyMaterial = await crypto.subtle.importKey(
            "raw", enc.encode(password), "PBKDF2", false, ["deriveKey"]
        );
        return crypto.subtle.deriveKey(
            { name: "PBKDF2", salt: enc.encode(username), iterations: 100000, hash: "SHA-256" },
            keyMaterial,
            { name: "AES-GCM", length: 256 },
            true,
            ["encrypt", "decrypt"]
        );
    },

    async storeKey(key) {
        const exported = await crypto.subtle.exportKey("raw", key);
        sessionStorage.setItem("enc_key", JSON.stringify(Array.from(new Uint8Array(exported))));
    },

    async loadKey() {
        const stored = sessionStorage.getItem("enc_key");
        if (!stored) return null;
        const keyData = new Uint8Array(JSON.parse(stored));
        return crypto.subtle.importKey("raw", keyData, { name: "AES-GCM" }, false, ["encrypt", "decrypt"]);
    },

    async encryptFile(file, key) {
        const iv = crypto.getRandomValues(new Uint8Array(12));
        const arrayBuffer = await file.arrayBuffer();
        const encrypted = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, arrayBuffer);
        const result = new Uint8Array(12 + encrypted.byteLength);
        result.set(iv, 0);
        result.set(new Uint8Array(encrypted), 12);
        return new Blob([result], { type: "application/octet-stream" });
    },

    async decryptFile(blob, key) {
        const arrayBuffer = await blob.arrayBuffer();
        const data = new Uint8Array(arrayBuffer);
        const iv = data.slice(0, 12);
        const encrypted = data.slice(12);
        return crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, encrypted);
    }
};
