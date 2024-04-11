<template>
    <d-card class="card-demo-basic">
        <template #avatar>
            <d-avatar name="DevUI"></d-avatar>
        </template>
        <template #title> DEVUI Course </template>
        <template #subtitle class="card-demo-icon"> <d-icon name="company-member"></d-icon><span>DevUI</span>
        </template>
        <template #content>
            DEVUI is a free open-source and common solution for the front end of enterprise mid- and back-end products.
            Its design values are
            basedon...
        </template>
        <template #actions>
            <div class="card-block"><d-icon name="like"></d-icon><span>12</span></div>
            <div class="card-block"><d-icon name="star-o"></d-icon><span>8</span></div>
            <div class="card-block"><d-icon name="message"></d-icon><span>8</span></div>
        </template>
    </d-card>
</template>
<style lang="less">
.card-demo-basic {
    cursor: pointer;

    .card-demo-icon {
        cursor: pointer;
        font-size: 16px;
        margin-right: 8px;
        vertical-align: middle;
    }

    .card-demo-icon+span {
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

    .action-text {
        color: #8a8e99;
    }
}
</style>