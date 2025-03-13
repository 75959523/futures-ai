document.addEventListener("DOMContentLoaded", function () {
    // 定义更新数据的函数
    function updateData() {
      fetch("http://localhost:8000/data")
        .then((response) => response.json())
        .then((data) => {
          // 获取页面中所有交易所区块
          const exchangeNodes = document.querySelectorAll("section.exchange-section");
          if (exchangeNodes.length < 3) {
            console.error("未找到足够的交易所节点");
            return;
          }
          // 按页面顺序分别对应 OKX、Binance、Bybit
          const exchangeSections = {
            okx: exchangeNodes[0],
            binance: exchangeNodes[1],
            bybit: exchangeNodes[2],
          };
  
          // JSON 中合约类型与页面卡片标题映射
          const contractMapping = {
            u: "U本位合约",
            coin: "币本位合约",
            usdc: "USDC合约",
          };
  
          // 根据 data-label 查找卡片内的 .data-item 并更新其 .data-value
          // 当 labelText 为 “资金费率” 时，根据数值决定颜色（默认绿色，小于 0.005；大于等于 0.005 则红色）
          function updateCardItem(card, labelText, newValue) {
            const dataItem = Array.from(card.querySelectorAll(".data-item")).find(item => {
              const labelEl = item.querySelector(".data-label");
              return labelEl && labelEl.textContent.trim() === labelText;
            });
            if (dataItem && newValue != null && newValue !== "") {
              const valueEl = dataItem.querySelector(".data-value");
              if (valueEl) {
                valueEl.textContent = newValue;
                if (labelText === "资金费率") {
                  // 去掉百分号并转换为数字
                  const num = parseFloat(newValue.replace("%", ""));
                  if (!isNaN(num)) {
                    if (num >= 0.005) {
                      // >= 0.005% 显示红色
                      valueEl.classList.remove("positive");
                      valueEl.classList.add("negative");
                    } else {
                      // 默认显示绿色
                      valueEl.classList.remove("negative");
                      valueEl.classList.add("positive");
                    }
                  }
                }
              }
            }
          }
  
          let overallTotal = 0; // 用于累计所有交易所的总值
  
          // 遍历每个交易所
          Object.keys(data).forEach((exchange) => {
            if (!exchangeSections[exchange]) {
              console.warn(`未找到 ${exchange} 对应的 DOM 节点`);
              return;
            }
            // 数据在 "btc" 层下
            const symbolData = data[exchange]["btc"];
            let exchangeTotal = 0;
  
            // 遍历每种合约类型
            Object.keys(contractMapping).forEach((contractKey) => {
              const cardTitle = contractMapping[contractKey];
              // 根据卡片标题查找对应的 data-card 元素
              const card = Array.from(
                exchangeSections[exchange].querySelectorAll(".data-card")
              ).find((card) => {
                const h3 = card.querySelector("h3");
                return h3 && h3.textContent.trim() === cardTitle;
              });
              if (!card) return;
  
              const contractData = symbolData[contractKey];
              if (contractData) {
                // 分别取出资金费率、未平仓量和标记价格，并验证数据是否存在
                const fundingRate =
                  contractData.funding_rate && contractData.funding_rate.value && contractData.funding_rate.value !== ""
                    ? contractData.funding_rate.value
                    : null;
                const openInterest =
                  contractData.open_interest && contractData.open_interest.value && contractData.open_interest.value !== ""
                    ? contractData.open_interest.value
                    : null;
                const markPrice =
                  contractData.mark_price && contractData.mark_price.value && contractData.mark_price.value !== ""
                    ? contractData.mark_price.value
                    : null;
  
                // 更新资金费率
                updateCardItem(card, "资金费率", fundingRate);
                // 更新未平仓合约量
                if (openInterest != null) {
                  // 对于币安和 Bybit 的币本位合约，单位显示为“亿”，其他情况下显示“BTC”
                  const unit = ((exchange === "binance" || exchange === "bybit") && contractKey === "coin")
                    ? " 亿"
                    : " BTC";
                  updateCardItem(card, "未平仓合约量", openInterest + unit);
                }
                // 更新标记价格
                updateCardItem(card, "标记价格", markPrice != null ? "$" + Number(markPrice).toFixed(2) : null);
  
                // 当 openInterest 和 markPrice 均存在且为有效数字时进行计算
                if (
                  openInterest != null &&
                  markPrice != null &&
                  !isNaN(openInterest) &&
                  !isNaN(markPrice)
                ) {
                  const product = openInterest * markPrice;
                  // 币安和 Bybit 的币本位合约 (coin) 不计入交易所汇总
                  if (!((exchange === "binance" || exchange === "bybit") && contractKey === "coin")) {
                    exchangeTotal += product;
                  }
                }
              }
            });
  
            // 更新该交易所的汇总卡片（标题为 “交易所汇总”）
            const summaryCard = Array.from(
              exchangeSections[exchange].querySelectorAll(".data-card")
            ).find((card) => {
              const h3 = card.querySelector("h3");
              return h3 && h3.textContent.trim() === "交易所汇总";
            });
            if (summaryCard) {
              const summaryValueEl = summaryCard.querySelector(".data-value");
              if (summaryValueEl) {
                summaryValueEl.textContent = (exchangeTotal / 1e8).toFixed(2) + " 亿";
              }
            }
            overallTotal += exchangeTotal;
          });
  
          // 更新总体概览中的“总未平仓合约量”
          const overallSummary = document.querySelector(".summary-card .data-value.highlight");
          if (overallSummary) {
            overallSummary.textContent = (overallTotal / 1e8).toFixed(2) + " 亿";
          }
        })
        .catch((error) => {
          console.error("获取数据出错:", error);
        });
    }
  
    // 初次获取数据
    updateData();
    // 每 0.2 秒更新一次数据
    setInterval(updateData, 200);
  });