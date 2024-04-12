<template>
    <div class="content" @click="router.push({ path: '/' })">
        <d-card class="card-demo-custom-area" :align="'spaceBetween'">
            <div class="custom-avatar">
                <d-avatar imgSrc="https://devui.design/components/assets/logo.svg" :width="48" :height="48"
                    :isRound="false"></d-avatar>
            </div>
            <template v-slot:title>
                <div>页面不存在,点击回主页</div>
            </template>
        </d-card>
    </div>

</template>
<script setup>
// import { useRouter } from 'vue-router'
const router = useRouter() 
</script>
<style lang="less">
.content {
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.card-demo-custom-area {
    cursor: pointer;
    width: 320px;
    display: flex;
    justify-content: center;
    align-items: center;

    .icon {
        cursor: pointer;
        font-size: 16px;
        margin-right: 8px;
        vertical-align: middle;
    }

    .icon+span {
        vertical-align: middle;
    }

    .card-block {
        margin-right: 16px;

        i {
            cursor: pointer;
            font-size: 16px;
            margin-right: 8px;
            vertical-align: middle;
        }

        i+span {
            vertical-align: middle;
        }
    }

    .card-container {
        width: 350px;
    }

    img {
        max-width: none;
    }

    .action-text {
        color: #8a8e99;
    }

    .custom-avatar {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;

        .custom-star-action {
            font-size: 20px;
            cursor: pointer;
        }
    }
}
</style>