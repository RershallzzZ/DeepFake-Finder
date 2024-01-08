<template>
    <div class="user-activity">
        <el-timeline>
            <el-timeline-item
                v-for="(item, index) of timeline"
                :key="index"
                :timestamp="item.timestamp"
                placement="top"
            >
                <el-card>
                    <div class="post">
                        <div class="user-block">
                            <img class="img-circle" :src="item.avatar" />
                            <span class="username text-muted">{{ item.author }}</span>
                            <span class="description" v-html="item.activity"></span>
                            <span class="url">
                                <el-link
                                    :href="item.url"
                                    target="_blank"
                                    type="primary"
                                    style="font-weight: 500;font-size:15px;"
                                >
                                    {{ item.url }}
                                </el-link>
                            </span>
                        </div>

                        <p>
                            {{ item.introduction }}
                        </p>
                        <ul class="list-inline">
                            <li style="margin-bottom:6px;">
                                <span class="link-black text-sm">
                                    <el-tag :type="item.analyzed | analyzedTagFilter">
                                        {{ item.analyzed | analyzedFilter }}
                                    </el-tag>
                                </span>
                            </li>
                            <li style="margin-bottom:6px;">
                                <span class="link-black text-sm">
                                    <el-tag effect="plain">{{ item.category }}</el-tag>
                                </span>
                            </li>
                        </ul>
                        <hr style="height:1px;border:none;border-top:1px solid #d2d6de;" />
                        <video style="width:100%;margin-top:6px;" controls :src="item.videoUrl"></video>
                    </div>
                </el-card>
            </el-timeline-item>
        </el-timeline>
    </div>
</template>

<script>
const avatarPrefix = '?imageView2/1/w/80/h/80'
const analyzedOption = [
    { type: 1, name: '无疑似' },
    { type: 2, name: '低疑似' },
    { type: 3, name: '中疑似' },
    { type: 4, name: '高疑似' },
]
export default {
    data() {
        return {
            avatarPrefix,
            analyzedOption,
            timeline: [
                {
                    timestamp: '2020/5/26',
                    avatar:
                        'https://yt3.ggpht.com/a/AATXAJyel4xeAMeczs7Yavrze-nXn0ImJv6kmKTnQQ=s88-c-k-c0xffffffff-no-rj-mo',
                    author: `乳透社·小池塘Winnie the Pool`,
                    activity:
                        '发布视频&nbsp;&nbsp;<strong>' +
                        "习德塞在WHO大会上怒斥台湾" +
                        '</strong>&nbsp;&nbsp;2020-05-14',
                    url: 'https://www.youtube.com/watch?v=CsPhbUeUsMk&t=96s',
                    introduction: `原视频：谭德塞点名台湾「真的够了」 狂骂3分钟影像全曝光`,
                    analyzed: 4,
                    category: '其他',
                    videoUrl: 'http://127.0.0.1:5000/video/youtube/666.mp4',
                },
                {
                    timestamp: '2020/5/26',
                    avatar: 'https://pic.downk.cc/item/5ed3e796c2a9a83be5eac6ec.jpg',
                    author: 'deepfake',
                    activity:
                        '发布视频&nbsp;&nbsp;<strong>' +
                        '【后浪】王思聪《后浪》演讲' +
                        '</strong>&nbsp;&nbsp;2020-05-16',
                    url: 'https://www.bilibili.com/video/BV1TQ4y1K7vd?from=search',
                    introduction: `国民老公后浪.`,
                    analyzed: 3,
                    category: '娱乐',
                    videoUrl: 'http://127.0.0.1:5000/video/bilibili/2.mp4',
                },
                {
                    timestamp: '2020/5/25',
                    avatar:
                        'https://yt3.ggpht.com/a/AATXAJw9LJc02NG3Ustgw8ZxD5IgXdzKFVP_-D3oNA=s100-c-k-c0xffffffff-no-rj-mo',
                    author: '纲冈刚',
                    activity: '发布视频&nbsp;&nbsp;<strong>' + '新垣结衣AI换脸郭德纲' + '</strong>&nbsp;&nbsp;2019-07-30',
                    url: 'https://www.bilibili.com/video/BV1FJ41137ZA?from=search',
                    introduction: `你们的老婆新垣结衣换脸郭德纲，这谁受得了`,
                    analyzed: 3,
                    category: '科技',
                    videoUrl: 'http://127.0.0.1:5000/video/bilibili/20.mp4',
                },
                {
                    timestamp: '2020/5/7',
                    avatar:
                        'https://yt3.ggpht.com/a/AATXAJyJxk3k4jg4Xrs522M50fKmTAo261qPJjYvPg=s100-c-k-c0xffffffff-no-rj-mo',
                    author: '币大爷',
                    activity:
                        '发布视频&nbsp;&nbsp;<strong>' +
                        '迪丽热巴做主播' +
                        '</strong>&nbsp;&nbsp;2019-07-31',
                    url: 'https://www.youtube.com//watch?v=gBdl9ymqETM',
                    introduction: `https://www.youtube.com/watch?v=JQGQcQrTy38 毫无违和感，van全一致`,
                    analyzed: 4,
                    category: '娱乐',
                    videoUrl: 'http://127.0.0.1:5000/video/bilibili/3.mp4',
                },
            ],
        }
    },
    filters: {
        analyzedFilter(type) {
            //过滤器中无法使用this

            const analyzedObj = analyzedOption.find(obj => obj.type === type)
            return analyzedObj ? analyzedObj.name : null
        },
        analyzedTagFilter(tagType) {
            const tagTypeMap = [
                {
                    type: 1,
                    name: 'success',
                },
                {
                    type: 2,
                    name: '',
                },
                {
                    type: 3,
                    name: 'warning',
                },
                {
                    type: 4,
                    name: 'danger',
                },
            ]
            const tagTypeObj = tagTypeMap.find(obj => obj.type === tagType)
            return tagTypeObj ? tagTypeObj.name : null
        },
    },
}
</script>

<style lang="scss" scoped>
.user-activity {
    .user-block {
        .username,
        .description,
        .url {
            display: block;
            margin-left: 70px;
            padding: 2px 0;
        }

        .username {
            font-size: 16px;
            color: #000;
        }

        :after {
            clear: both;
        }

        .img-circle {
            border-radius: 50%;
            width: 60px;
            height: 60px;
            float: left;
        }

        span {
            font-weight: 500;
            font-size: 15px;
        }
    }

    .post {
        font-size: 14px;
        border-bottom: 1px solid #d2d6de;
        margin-bottom: 15px;
        padding-bottom: 15px;
        color: #666;

        .image {
            width: 100%;
            height: 100%;
        }

        .user-images {
            padding-top: 20px;
        }
    }

    .list-inline {
        padding-left: 0;
        margin-left: -5px;
        list-style: none;

        li {
            display: inline-block;
            padding-right: 5px;
            padding-left: 5px;
            font-size: 15px;
        }

        .link-black {
            &:hover,
            &:focus {
                color: #999;
            }
        }
    }
}

.box-center {
    margin: 0 auto;
    display: table;
}

.text-muted {
    color: #777;
}
</style>
