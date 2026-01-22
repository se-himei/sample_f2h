// Image assets
const imgIcon = "https://www.figma.com/api/mcp/asset/7136254f-4a68-4d38-94a7-af8efb31bc00";
const imgVector = "https://www.figma.com/api/mcp/asset/25f6f411-ce6a-44ed-8cd6-03b0bbbf9a5f";
const imgVector1 = "https://www.figma.com/api/mcp/asset/8b8c14a3-8ab5-4fad-a9bd-d4a1f64909c3";
const imgIcon1 = "https://www.figma.com/api/mcp/asset/da36f345-d295-4874-b90c-169d15b99c26";
const imgIcon2 = "https://www.figma.com/api/mcp/asset/65929782-6a6d-429b-a780-b701c522ac54";
const imgIcon3 = "https://www.figma.com/api/mcp/asset/5b3b0d7b-0b3f-4802-b97a-6399203cdc27";
const imgIcon4 = "https://www.figma.com/api/mcp/asset/6ec6a0dc-9d29-4c56-aec8-13f570bd94aa";
const imgIcon5 = "https://www.figma.com/api/mcp/asset/d5784944-f130-4eaf-8069-2edd5001f7c3";

interface MedicationCardProps {
  name: string;
  description: string;
  frequency: string;
  hospital: string;
  prescriptionDate: string;
  times: string[];
}

function MedicationCard({ name, description, frequency, hospital, prescriptionDate, times }: MedicationCardProps) {
  return (
    <article className="bg-white border border-gray-100 rounded-[14px] shadow-sm p-4">
      <div className="flex gap-3 mb-3">
        <div className="w-12 h-12 bg-blue-100 rounded-[10px] flex items-center justify-center shrink-0">
          <img src={imgIcon1} alt="Medication" className="w-6 h-6" />
        </div>
        <div className="flex-1 flex flex-col gap-1">
          <h3 className="text-base text-gray-900">{name}</h3>
          <p className="text-sm text-gray-600">{description}</p>
          <div className="flex gap-3">
            <span className="flex items-center gap-1 text-xs text-gray-500">
              <img src={imgIcon2} alt="Clock" className="w-3 h-3" />
              <span>{frequency}</span>
            </span>
            <span className="flex items-center gap-1 text-xs text-gray-500">
              <img src={imgIcon3} alt="Hospital" className="w-3 h-3" />
              <span>{hospital}</span>
            </span>
          </div>
        </div>
        <div className="flex flex-col gap-1 text-right shrink-0">
          <span className="text-xs text-gray-500">処方日</span>
          <span className="text-xs text-gray-700">{prescriptionDate}</span>
        </div>
      </div>
      <div className="flex gap-2 pt-3 border-t border-gray-100">
        {times.map((time, index) => (
          <span key={index} className="bg-blue-50 text-blue-600 text-xs px-3 py-1 rounded-full">
            {time}
          </span>
        ))}
      </div>
    </article>
  );
}

export default function MedicationRecordApp() {
  const medications = [
    {
      name: "アモキシシリン錠250mg",
      description: "気管支炎の治療",
      frequency: "1日3回",
      hospital: "東京中央クリニック",
      prescriptionDate: "2025年12月20日",
      times: ["08:00", "12:30", "19:00"],
    },
    {
      name: "ロキソプロフェンNa錠60mg",
      description: "痛み止め",
      frequency: "1日2回",
      hospital: "都立総合病院",
      prescriptionDate: "2025年12月15日",
      times: ["09:00", "21:00"],
    },
    {
      name: "オメプラゾール錠20mg",
      description: "胃酸の分泌を抑える",
      frequency: "1日1回",
      hospital: "東京中央クリニック",
      prescriptionDate: "2025年11月10日",
      times: ["07:30"],
    },
  ];

  return (
    <div className="w-[564px] min-h-[876px] mx-auto bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-500 to-blue-600 px-4 pt-6 h-48 shadow-lg">
        <div className="flex flex-col gap-4">
          <div className="flex justify-between items-center h-12">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center">
                <img src={imgIcon} alt="Icon" className="w-7 h-7" />
              </div>
              <div className="flex flex-col">
                <p className="text-sm text-white/90">お薬手帳</p>
                <p className="text-xs text-white/75">田中 太郎 様</p>
              </div>
            </div>
            <button className="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center">
              <div className="w-6 h-6 relative">
                <img src={imgVector} alt="Settings" className="absolute inset-0" />
                <img src={imgVector1} alt="Settings" className="absolute inset-0" />
              </div>
            </button>
          </div>
          <div className="bg-white/20 rounded-[10px] p-4 h-20">
            <div className="grid grid-cols-3 gap-4 h-12">
              <div className="flex flex-col text-center">
                <p className="text-2xl text-white">3</p>
                <p className="text-xs text-white/90">服用中の薬</p>
              </div>
              <div className="flex flex-col text-center">
                <p className="text-2xl text-white">12</p>
                <p className="text-xs text-white/90">今月の服用</p>
              </div>
              <div className="flex flex-col text-center">
                <p className="text-2xl text-white">2</p>
                <p className="text-xs text-white/90">処方箋</p>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Tab Navigation */}
      <nav className="bg-white border-b border-gray-200 h-[59px]">
        <div className="flex h-[58px]">
          <button className="flex-1 flex items-center justify-center gap-2 border-b-2 border-blue-600">
            <img src={imgIcon4} alt="List" className="w-5 h-5" />
            <span className="text-base text-blue-600">お薬リスト</span>
          </button>
          <button className="flex-1 flex items-center justify-center gap-2">
            <img src={imgIcon5} alt="Calendar" className="w-5 h-5" />
            <span className="text-base text-gray-500">服用カレンダー</span>
          </button>
        </div>
      </nav>

      {/* Medication List */}
      <main className="p-4 flex flex-col gap-4">
        {medications.map((med, index) => (
          <MedicationCard key={index} {...med} />
        ))}
      </main>
    </div>
  );
}
