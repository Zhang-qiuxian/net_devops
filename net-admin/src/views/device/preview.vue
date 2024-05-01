<template>
    <el-scrollbar>
        <el-row :gutter="20">
            <el-col :span="6" v-for="i in 32" :key="i">
                <el-card style="max-width: 480px">
                    <template #header>
                        <div class="card-header">
                            <span>Card name</span>
                        </div>
                    </template>
                    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
                    <template #footer>Footer content</template>
                </el-card>
            </el-col>
        </el-row>
    </el-scrollbar>
</template>
<style lang="scss" scoped>
.el-row {
    margin-left: 0 !important;
    margin-right: 0px !important;

    .el-col {
        margin-top: 10px;
    }
}
</style>