## audioDistribution

>  一个简单的进行音频文件分发的后端服务

### Usage

#### 上传任务

##### URL

> http://<deploy_address>:<deploy_port>/getter/task/

##### Parameters

```json
{
    "file_path": "<音频文件路径>"
}
```

##### Response

```json
{
    "code": 200,
    "msg": "Successfully add a task."
}
```

##### Note

- 一次上传一个任务，系统自动提取音频并获取时长，存入后台数据库，等待识别
- 仓库内预编写了批量上传工具代码，在`scripts/upload_task.py`，该文件读取预定义tsv文件并进行任务上传，tsv文件按行存储每个音频文件的路径

#### 获取一个音频文件进行识别

##### URL

> http://<deploy_address>:<deploy_port>/getter/audio/

##### Parameters

> 无

##### Response

- 系统自动查询当前仓库内未经识别的一个音频文件并返回给客户端进行下载

- 文件进行流传输，是一个标准的`HttpFileResponse`

- 文件名为该文件在仓库内的id，是唯一定位该文件的标识符，请客户端务必妥善保存，后面更新该文件文本时需要使用

- 若无需要识别的文件，返回如下

  ```json
  {
      "code": 404,
      "msg": "There's no more task."
  }
  ```

#### 识别好一个音频文件进行文本回传

##### URL

> http://<deploy_address>:<deploy_port>/getter/transcript/

##### Parameters

```json
{
    "task_id": <需要更新的音频文件id，即上述文件名，不需要引号>,
    "transcript": "<识别的对应文本>"
}
```

#### Response

```json
// 更新成功
{
    "code": 200,
    "msg": "Successfully update the task."
}

// 更新失败
{
    "code": 404,
    "msg": "Cannot find the right task, please check your task id"
}
```

#### 导出已经被识别并从未导出的数据库记录为tsv文件

##### URL

> http://<deploy_address>:<deploy_port>/getter/data/

##### Parameters

> 无

##### Response

- 系统自动查询库存记录，去除已导出、未标记的记录并整理成一个tsv文件返回，供客户端进行下载

- 若无可导出记录，返回如下

  ```json
  {
      "code": 404,
      "msg": "There's no more unexported data."
  }
  ```

  