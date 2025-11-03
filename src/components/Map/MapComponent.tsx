import { useEffect, useRef, useState } from 'react';
import { getApiConfig } from '../../utils/config';
import { MapService } from '../../services/api';

interface MapComponentProps {
  destination?: string | null;
  location?: { lng: number; lat: number } | null;
}

export default function MapComponent({ destination, location }: MapComponentProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<any>(null);
  const markerRef = useRef<any>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  // 初始化地图
  useEffect(() => {
    const config = getApiConfig('amap');
    if (!config?.jsApiKey) {
      console.warn('高德地图API未配置');
      return;
    }

    // 如果地图脚本已加载，直接创建地图
    if (window.AMap && mapRef.current && !mapInstanceRef.current) {
      // @ts-ignore
      const map = new window.AMap.Map(mapRef.current, {
        zoom: 10,
        center: [116.397428, 39.90923], // 默认北京
      });
      mapInstanceRef.current = map;
      setMapLoaded(true);
      return;
    }

    // 动态加载高德地图脚本
    const script = document.createElement('script');
    script.src = `https://webapi.amap.com/maps?v=2.0&key=${config.jsApiKey}`;
    script.async = true;
    script.onload = () => {
      if (window.AMap && mapRef.current && !mapInstanceRef.current) {
        // @ts-ignore
        const map = new window.AMap.Map(mapRef.current, {
          zoom: 10,
          center: [116.397428, 39.90923], // 默认北京
        });
        mapInstanceRef.current = map;
        setMapLoaded(true);
      }
    };
    document.head.appendChild(script);

    return () => {
      // 清理脚本
      if (document.head.contains(script)) {
        document.head.removeChild(script);
      }
    };
  }, []);

  // 当地址或位置变化时，更新地图
  useEffect(() => {
    if (!mapLoaded || !mapInstanceRef.current) return;

    const updateMap = async () => {
      try {
        let targetLocation: { lng: number; lat: number } | null = null;

        // 如果提供了位置坐标，直接使用
        if (location) {
          targetLocation = location;
        } 
        // 如果提供了目的地名称，进行地理编码
        else if (destination) {
          const mapService = new MapService();
          targetLocation = await mapService.geocode(destination);
        }

        if (targetLocation) {
          const map = mapInstanceRef.current;
          
          // 设置地图中心
          map.setCenter([targetLocation.lng, targetLocation.lat]);
          map.setZoom(13);

          // 清除旧标记
          if (markerRef.current) {
            map.remove(markerRef.current);
          }

          // 添加新标记
          // @ts-ignore
          const marker = new window.AMap.Marker({
            position: [targetLocation.lng, targetLocation.lat],
            title: destination || '目的地',
          });
          map.add(marker);
          markerRef.current = marker;
        }
      } catch (error) {
        console.error('更新地图失败:', error);
      }
    };

    updateMap();
  }, [destination, location, mapLoaded]);

  return (
    <div className="w-full h-full relative">
      <div ref={mapRef} className="w-full h-full" />
      {!mapLoaded && (
        <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
          <div className="text-gray-500">加载地图中...</div>
        </div>
      )}
    </div>
  );
}

// 扩展Window类型以支持高德地图
declare global {
  interface Window {
    AMap: any;
  }
}

