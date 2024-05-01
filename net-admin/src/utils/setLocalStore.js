

export default function setLocalStore(key) {
    return `${import.meta.env.VITE_STORE_KEY}-${key}`
}