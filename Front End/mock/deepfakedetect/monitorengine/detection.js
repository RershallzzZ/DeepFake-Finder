import Mock from 'mockjs'

const List = {
    total:'@integer(100,200)',
    'list|10':[
        {
            'id|+1':1,
            'state|1':['-1','0','1'],
            'analyzed|1':['0','1','2','3','4'],
            crawl_time:'@datetime',
            url:'@url("http","test.com")',
            title:'@ctitle(5,10)',
            duration:'@datetime(mm:ss)',
            upload_time:"@datetime('yyyy-MM-dd')",
            'category|1': ['政治', '娱乐', '科技', '其他'], // 4选 其1
        }
    ]
}


export default[
    //搜索
    {
        url:'/deepfake-finder/monitorengine/detection/list/search',
        type:'post',
        response: _ => {
            return{
                code:20000,
                data:List
            }
        }
    },

    //开始手动检测
    {
        url:'/deepfake-finder/monitorengine/detection/manual',
        type:'post',
        response: _ => {
            return{
                code:20000,
                data:'所选视频开始检测'
            }
        }        
    },

    //开始自动检测
    {
        url:'/deepfake-finder/monitorengine/detection/auto/begin',
        type:'post',
        response: _ => {
            return{
                code:20000,
                data:'开始自动检测'
            }
        }              
    },

    //停止自动检测
    {
        url:'/deepfake-finder/monitorengine/detection/auto/stop',
        type:'post',
        response: _ => {
            return{
                code:20000,
                data:'停止自动检测'
            }
        }              
    }
]
