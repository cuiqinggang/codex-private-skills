# RAPTOR / STARSHIP — 工程迭代类比案例

> 本文是工程类比，不是本技能第一性原理公式的理论来源。

## 为什么保留

Starship/Raptor 展示：固定高层目标 -> 真实硬件进入真实环境 -> 暴露限制/失败机制 -> 删除/集成/重构 -> 再测试 -> 新证据反馈下一代。

SpaceX 官方资料明确把 real-world testing、快速识别改进点、验证解决方案和 lessons learned 直接反馈到下一代设计作为 Starship 开发方式。

## Raptor 3 的“去重甲 / 集成”类比

SpaceX 2026 官方更新列出：Raptor 3 海平面版本 250 tf（Raptor 2 为 230 tf）；真空版本 275 tf（前代 258 tf）；海平面发动机质量 1,525 kg（前代 1,630 kg）；传感器与控制器内部集成并由发动机热防护覆盖，从而取消独立 engine shrouds；通过发动机本体、vehicle-side commodities 和支撑硬件简化，车辆级每台发动机约减少 1 吨质量。

对本技能的启发：

```text
EXTERNAL WRAPPER / SUPPORT
-> ASK WHY REQUIRED
-> INTEGRATE INTO CORE WHEN PHYSICALLY POSSIBLE
-> DELETE REDUNDANT INTERFACES
-> REDUCE CRITICAL-PATH / MASS / FAILURE SURFACE
```

## 递归真实测试

SpaceX 官方表示自 Flight 1 起通过 active flight-test campaign 推进设计，最大化 real-world testing，快速证明能力、找出改进区域、验证解决方案；ground/flight lessons 直接进入后续代际。官方同一更新给出 Raptor 2 超过 226,000 秒运行、Raptor 3 超过 40,000 秒运行。

映射：`MODEL -> REAL TEST -> EVIDENCE -> MODEL UPDATE -> NEXT DESIGN`。

## 与本技能的区别

本技能把时间定义为固定 hard constraints 下唯一优化目标；SpaceX 官方同时考虑推力、质量、可靠性、复用、成本、生产、热防护等，因此不能声称 SpaceX 官方以时间为唯一指标。

## 官方资料

- https://new.spacex.com/updates
- https://new.spacex.com/vehicles/starship
- https://new.spacex.com/content/starship
- https://www.nasa.gov/blogs/missions/2023/09/14/spacex-completes-engine-tests-for-nasas-artemis-iii-moon-lander/

## 图片参考

### Raptor 1 / 2 / 3 外观演化

![Raptor engine evolution](https://images.squarespace-cdn.com/content/v1/670d65270f12627b6158f730/0acab4c5-c8f3-4cb5-928a-6ff945d9ec5f/raptor%2B3.jpeg?format=1500w)

来源：https://www.gram-dynamics.com/actualite/le-raptor-3-un-moteur-avanc-pour-lavenir-spatial

### Raptor 3 单机视觉参考

![Raptor 3](https://danielmarin.naukas.com/files/2024/08/GUEhKc9a0AA93nW-scaled.jpeg)

来源：https://danielmarin.naukas.com/2024/08/05/presentacion-en-sociedad-del-raptor-3-le-moteur-que-propulsera-la-starship-de-spacex/

图片只用于外观参考，性能事实以 SpaceX/NASA 官方资料为准。
