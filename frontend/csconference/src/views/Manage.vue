<template>
    <div class="manage">
        <el-row>
            <el-col :span="20" :offset="2">
                <el-form label-width="80px" class="search">
                    <el-form-item label="查询语句">
                        <el-input type="textarea" :rows="1" placeholder="请输入内容" v-model="textarea"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit" size="medium">查询</el-button>
                    </el-form-item>
                </el-form>
                <el-divider></el-divider>
                <el-card>
                    <el-table
                        ref="table"
                        :data="tableData"
                        stripe
                        style="width: 100%"
                        max-height="800"
                    >
                        <el-table-column fixed type="index" width="40"></el-table-column>
                        <el-table-column fixed type="expand" width="80">
                            <template slot-scope="scope">
                                <el-form
                                    label-position="left"
                                    inline
                                    class="demo-table-expand"
                                    label-width="100px"
                                >
                                    <el-form-item
                                        v-for="(label, index) in labels"
                                        :key="index"
                                        :label="label[1]"
                                    >
                                        <span>{{ scope.row[label[0]] }}</span>
                                    </el-form-item>
                                    <span class="fold" @click="foldRow(scope.row)">收起</span>
                                </el-form>
                            </template>
                        </el-table-column>
                        <el-table-column prop="abbr" label="简称" width="80" sortable></el-table-column>
                        <el-table-column prop="name" label="会议全称" min-width="240" sortable></el-table-column>
                        <el-table-column prop="s_date" label="开始日期" width="120" sortable></el-table-column>
                        <el-table-column prop="e_date" label="结束日期" width="120" sortable></el-table-column>
                        <el-table-column prop="paper_date" label="截稿日期" width="120" sortable></el-table-column>
                        <!-- <el-table-column prop="noti_date" label="接收通知日期" width="120" sortable></el-table-column> -->
                        <!-- <el-table-column prop="year" label="年份" width="80" sortable></el-table-column> -->
                        <el-table-column prop="address" label="地址" width="120"></el-table-column>
                        <el-table-column prop="website" label="官网" width="140"></el-table-column>
                        <!-- <el-table-column prop="organization" label="组织" width="80"></el-table-column> -->
                        <!-- <el-table-column prop="rank_CCF" label="CCF" width="60"></el-table-column> -->
                        <!-- <el-table-column prop="rank_CORE" label="CORE" width="70"></el-table-column> -->
                        <!-- <el-table-column prop="rank_QUALIS" label="QUALIS" width="80"></el-table-column> -->
                        <!-- <el-table-column prop="indexes" label="可检索数据库" width="100"></el-table-column> -->
                        <el-table-column fixed="right" label="操作" width="160">
                            <template slot-scope="scope">
                                <el-button
                                    @click.native.prevent="deleteRow(scope.$index, tableData)"
                                    type="danger"
                                    size="small"
                                >删除</el-button>
                                <el-button
                                    @click.native.prevent="editRow(scope.$index, scope.row)"
                                    type="primary"
                                    size="small"
                                >编辑</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-card>
            </el-col>
        </el-row>

        <el-dialog title="修改信息" :visible.sync="dialogVisible" center :before-close="handleClose" width="70%">
            <el-form :model="form_data" label-position="top" inline class="demo-table-expand" size="small">
                <el-form-item
                    class="edit"
                    v-for="(label, index) in labels"
                    :key="index"
                    :label="label[1]"
                >
                    <el-input v-model="form_data[label[0]]"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="handleClose">取 消</el-button>
                <el-button type="primary" @click="handleConfirm">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>


<script>
export default {
    name: "manage",
    data() {
        return {
            textarea: "",
            tableData: [],
            labels: [
                ["name", "会议全称"],
                ["abbr", "简称"],
                ["year", "年份"],
                ["s_date", "开始日期"],
                ["e_date", "结束日期"],
                ["paper_date", "截稿日期"],
                ["noti_date", "接收通知日期"],
                ["address", "地址"],
                ["website", "官网"],
                ["organization", "组织"],
                ["rank_CCF", "CCF"],
                ["rank_CORE", "CORE"],
                ["rank_QUALIS", "QUALIS"],
                ["indexes", "可检索数据库"],
                ["description", "描述"]
            ],
            form_data: {},
            expands: [],
            dialogVisible: false
        };
    },
    methods: {
        onSubmit() {
            console.log(this.textarea);
            this.$axios.post('/api/sql', {sql: this.textarea})
                .then(res => {
                    console.log(res.data.data);
                    
                    this.tableData = res.data.data
                }).catch(err => {
                    console.log(err);
                })
        },
        deleteRow(index, rows) {
            rows.splice(index, 1);
        },
        editRow(index, row) {
            this.form_data = row;
            this.dialogVisible = true;
        },
        foldRow(row) {
            this.$refs.table.toggleRowExpansion(row, false)
        },
        handleClose() {
            this.form_data = [];
            this.dialogVisible = false;
        },
        handleConfirm() {
            this.dialogVisible = false;
        }
    }
};
</script>

<style lang="scss" scoped>
.manage {
    margin-bottom: 30px;
    .search {
        text-align: start;
    }
}
.demo-table-expand {
    font-size: 0;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 2px;
}
.demo-table-expand .el-form-item {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
    &:first-child,
    &:nth-last-child(2) {
        width: 100%;
    }
    &.edit:first-child, &.edit:last-child {
        width: 100%;
        /deep/ .el-form-item__content {
            width: 95%
        }
    }
    &.edit:nth-last-child(2) {
        width: 50%
    }
    /deep/ .el-form-item__content {
        width: 80%;
    }
    &.edit /deep/ .el-form-item__content {
        width: 90%;
    }
    &.edit /deep/ .el-form-item__label {
        padding: 10px 0 0 0;
    }
}

.fold {
    color: #409eff;
    font-size: 14px;
    float: right;
    cursor: pointer;
}

/deep/ .el-form label {
    color: #99a9bf;
}

/deep/ .el-table__expand-icon::after {
    content: "查看更多";
    color: #409eff;
    cursor: pointer;
}
/deep/ .el-table__expand-icon > i {
    display: none !important;
}

/deep/ .el-table__expand-icon--expanded {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
    &::after {
        content: "收起面板";
    }
}
</style>