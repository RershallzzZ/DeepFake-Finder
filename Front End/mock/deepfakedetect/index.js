const lineChartData = {
  year: [2018, 2019, 2020],
  "deepfakeVideo": [89,216,68],
  "downloadVideo": [154,377,138]
};

const pieChartData = {
  "high|1300-1500": 1,
  "medium|1300-1500": 1,
  "low|1500-1700": 1,
  "none|1800-2000": 1
};

const raddarChartData = {
  "youtube|4": ["@integer(800,1000)"],
  "bilibili|4": ["@integer(100,1000)"],
  "vimeo|4": ["@integer(500,1000)"]
};

const barChartData = {
  "politics|3":["@integer(50,100)"],
  "entertainment|3":["@integer(50,100)"],
  "tech|3":["@integer(50,100)"],
  "others|3":["@integer(50,100)"]
}

const detailData = {
  lineChartData,
  pieChartData,
  raddarChartData,
  barChartData,
  websites:['youtube','bilibili','vimeo']
};

const profileData = {
  "monitorWebsite": 3,
  "downloadVideo": 642,
  "detectVideo": 584,
  "deepfakeVideo": 384
};

export default [
  {
    url: "/deepfake-finder/profile",
    type: "get",
    response: _ => {
      return {
        code: 20000,
        data: profileData
      };
    }
  },
  {
    url: "/deepfake-finder/detail",
    type: "get",
    response: _ => {
      return {
        code: 20000,
        data: detailData
      };
    }
  }
];
